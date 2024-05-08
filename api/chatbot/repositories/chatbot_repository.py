from string import Template

from api.desing_patterns.creational_patterns.singleton.openai_singleton import OpenAISingleton
from api.desing_patterns.creational_patterns.singleton.chromadb_singleton import ChromaSingleton
from api.desing_patterns.creational_patterns.singleton.database_singleton import DatabaseSingleton

from ..utils.prompt_handlers.prompt_loader import load_prompt_file

import json


class ChatbotRepository():

    async def post_user_message(self, message:str, thread_id:str, procedure:str):

        procedure_found = await DatabaseSingleton.get_procedure(procedure)
        documents = await ChromaSingleton.search_similarity_procedure(message, procedure_found.file_name)
        prompt = Template(load_prompt_file('api/chatbot/prompts/chatbot_prompt.txt'))

        prompt = prompt.substitute(
            context=str.join('\n-----------------\n', [document.page_content for document in documents]),
            question=message
        )

        await OpenAISingleton.add_message(prompt, thread_id)
        msg = await OpenAISingleton.run_thread(thread_id)

        return msg


    async def create_thread(self):

        thread_id = await OpenAISingleton.create_conversation_thread()

        return thread_id


    async def delete_thread(self, thread_id:str):

        await OpenAISingleton.delete_conversation_thread(thread_id)
