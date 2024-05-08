import os
import chromadb
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from api.config import OPENAI_API_KEY, EMBEDDING_MODEL


embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)

persistent_client = chromadb.PersistentClient(path="./chroma_db")


import os

def leer_archivos_directorio(directorio):
    docs=[]
    # Verificar si el directorio existe
    if os.path.exists(directorio):
        # Obtener la lista de archivos en el directorio
        archivos = os.listdir(directorio)

        # Iterar sobre cada archivo en el directorio
        for archivo in archivos:
            # Obtener la ruta completa del archivo
            ruta_archivo = os.path.join(directorio, archivo)
            
            # Verificar si es un archivo regular
            if os.path.isfile(ruta_archivo):
                # Leer el contenido del archivo
                with open(ruta_archivo, 'r', encoding='utf-8') as f:
                    contenido = f.read()
                    d = Document(
                        page_content=contenido,
                        metadata={'name':ruta_archivo.split('\\')[-1:][0]}
                    )
                    docs.append(d)
            else:
                print(f"{archivo} no es un archivo regular.")
    else:
        print(f"El directorio {directorio} no existe.")
    
    return docs

# Directorio que deseas leer
directorio = 'documentos'

# Llamar a la función para leer los archivos del directorio
#docs = leer_archivos_directorio(directorio)


#from langchain_text_splitters import RecursiveCharacterTextSplitter

#text_splitter = RecursiveCharacterTextSplitter(
#    chunk_size=2000,
#    chunk_overlap=20,
#    length_function=len,
#    is_separator_regex=False,
#    separators=[
#        "\n\n",
#        "\n",
#    ]
#)

#docs = text_splitter.transform_documents(docs)

persistent_client.get_or_create_collection("tramites_jalisco")

#langchain_chroma = Chroma.from_documents(
#    documents=docs,
#    client=persistent_client,
#    collection_name="tramites_jalisco",
#    embedding=embeddings,
#)

db3 = Chroma(client=persistent_client, collection_name="tramites_jalisco", embedding_function=embeddings)
docs = db3.similarity_search('cuales son los requisitos?', k=5, filter={'name':'constanciadeantecedentesnopenales.txt'})
