from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

import chromadb
from api import config


__author__ = 'Ricardo'
__version__ = '0.1'


class ChromaSingleton():

    __client = None
    __embedding = None


    @classmethod
    def __get_connection(self, embedding):
        """
        This method create our client
        """

        client = chromadb.PersistentClient(path="./chroma_db")
 
        return Chroma(client=client, collection_name="tramites_jalisco", embedding_function=embedding)
 

    def __new__(cls, *args, **kwargs):
        
        if cls.__client==None:
            cls.__embedding = OpenAIEmbeddings(model=config.EMBEDDING_MODEL)
            cls.__client = cls.__get_connection(cls.__embedding)

        return cls.__client


    @classmethod
    async def search_similarity_procedure(cls, message:str, procedure_file:str):
        """
        This method search the similarity in a text given inside ChromaDB

        :param message: an string beging our text to query
        :param procedure: an string beging our metadata file name to query
        :return: a list with our documents
        """

        docs = await cls.__client.asimilarity_search(message, k=5, filter={'name':f'{procedure_file}.txt'})
        
        return docs
