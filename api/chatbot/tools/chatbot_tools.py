from typing import Type
import json

from langchain.tools import BaseTool
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.chains import create_sql_query_chain
from langchain_community.utilities import SQLDatabase
from langchain.pydantic_v1 import BaseModel, Field

from ... import config
from ..desing_patterns.creational_patterns.singleton.gemini_singleton import GeminiSingleton
from ..desing_patterns.creational_patterns.singleton.chromadb_singleton import ChromaSingleton
from ..utils.prompt_handlers.prompt_loader import load_prompt_file


__author__ = 'Ricardo'
__version__ = '0.1'


class VeracityToolInput(BaseModel):
    message: str = Field(description="message to answer")


class VeracityTool(BaseTool):
    name = "VeracityTool"
    description = "useful for when you need to do similarity search in chromadb"
    args_schema: Type[BaseModel] = VeracityToolInput

    def _run(self) -> str:
        return NotImplementedError("VeracityTool does not support sync")

    async def _arun(self, message:str) -> str:

        prompt = load_prompt_file("api/chatbot/prompts/general_answer_prompt.txt")

        chat_template = ChatPromptTemplate.from_messages([
            HumanMessagePromptTemplate.from_template(prompt)
        ])

        formatted_chat_template = chat_template.format_messages(message=message)
        ai = await GeminiSingleton.post_user_message(formatted_chat_template)

        return {'msg':ai, 'memory':[f"ia: {ai}",]}


class ChromaToolInput(BaseModel):
    message: str = Field(description="message to embed and do similarity search in chromadb")


class ChromaTool(BaseTool):
    name = "ChromaTool"
    description = "useful for when you need to do similarity search in chromadb"
    args_schema: Type[BaseModel] = ChromaToolInput

    def _run(self) -> str:
        return NotImplementedError("ChromaTool does not support sync")

    async def _arun(self, message:str) -> str:
        docs = await ChromaSingleton.search_similarity_guitar(message)

        prompt = load_prompt_file("api/chatbot/prompts/chromadb_prompt.txt")
        context = ""

        for doc in docs:
            context += f'''
            pregunta: {doc.page_content}
            respuesta: {doc.metadata['answer']}
            '''

        chat_template = ChatPromptTemplate.from_messages([
            HumanMessagePromptTemplate.from_template(prompt)
        ])

        formatted_chat_template = chat_template.format_messages(context=context, message=message)
        ai = await GeminiSingleton.post_user_message(formatted_chat_template)

        return {'msg':ai, 'memory':[f"ia: {ai}",]}


class DatabaseToolInput(BaseModel):
    message: str = Field(description="message to become in sql query")


class DatabaseTool(BaseTool):
    name = "DatabaseTool"
    description = "useful for when you need to answer questions in a sql database"
    args_schema: Type[BaseModel] = DatabaseToolInput

    def _run(self) -> str:
        return NotImplementedError("DatabaseTool does not support sync")

    async def _arun(self, message:str) -> str:

        # generate sql query
        db = SQLDatabase.from_uri(config.DB_URL)
        chain = create_sql_query_chain(GeminiSingleton.get_client(), db)
        prompt = load_prompt_file("api/chatbot/prompts/sqldatabase_query_construction_prompt.txt")

        # run sql query
        result = await chain.ainvoke({"question": prompt.format(message=message)})
        result = db.run(result, fetch="cursor")
        data = list(result.mappings())
        
        # generate responde from sql query
        prompt = load_prompt_file("api/chatbot/prompts/sqldatabase_prompt.txt")
        msg = prompt.format(message=message, data=data)
        ai = await GeminiSingleton.post_user_message(msg)

        # eval response
        prompt = load_prompt_file("api/chatbot/prompts/sqldatabase_eval_prompt.txt")
        
        chat_template = ChatPromptTemplate.from_messages([
            HumanMessagePromptTemplate.from_template(prompt)
        ])

        formatted_chat_template = chat_template.format_messages(message=ai)
        eval = await GeminiSingleton.post_user_message(formatted_chat_template)

        images = []
        rows = []

        if eval=='True':
            for row in data:
                images.append(row['campo_imagen'])
                row = dict(row)
                del row['campo_imagen']
                rows.append(row)

        return {'msg':ai, 'images':images, 'memory':[f'ia: esta es informacion de base de datos sql {rows}', f'ia: {ai}',]}
