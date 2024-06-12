import sys

__import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
    

from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from api.desing_patterns.creational_patterns.singleton.openai_singleton import OpenAISingleton
from api.desing_patterns.creational_patterns.singleton.chromadb_singleton import ChromaSingleton
from api.desing_patterns.creational_patterns.singleton.database_singleton import DatabaseSingleton

import api


@asynccontextmanager
async def lifespan(app: FastAPI):
    print('startup')

    OpenAISingleton()
    ChromaSingleton()
    DatabaseSingleton()

    yield
    print('shutdown')


app = FastAPI(
    title="Asistente de tramites de jalisco",
    description="API para chatbot de asistencia de tramites de jalisco",
    version="0.1",
    lifespan=lifespan
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api.router)


from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.requests import Request


templates = Jinja2Templates(directory="frontend")
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")


@app.get("/frontend")
def read_root(request:Request):
    return templates.TemplateResponse('index.html', context={'request': request})


# ----------------CSRF TOKEN-----------------


#from fastapi_csrf_protect import CsrfProtect

# class CsrfSettings(BaseModel):
#     secret_key:str = config.SECRET_KEY
#     cookie_samesite:str = "strict"
#     cookie_secure:bool = True

# @CsrfProtect.load_config
# def get_csrf_config():
#     return CsrfSettings()

# @router.post("/submit")
# async def submit_data(request:Request, csrf_protect:CsrfProtect=Depends()):
#     await csrf_protect.validate_csrf(request)
#     return {'sdsd':'sdsd'}

# @router.get("/csrftoken")
# async def get_csrf_token(csrf_protect:CsrfProtect=Depends()):
#     response = Response(status_code=200)
#     response.set_cookie(key="csrf_token", value=csrf_protect.generate_csrf(), httponly=True, samesite="strict")
#     return response


# -------------------------------------------


#from fastapi.templating import Jinja2Templates
#from fastapi.staticfiles import StaticFiles
#from fastapi.requests import Request


#templates = Jinja2Templates(directory="frontend/build")
#app.mount("/static", StaticFiles(directory="frontend/build/static"), name="static")


#@app.get("/admin")
#def read_root(request:Request):
#    return templates.TemplateResponse('index.html', context={'request': request})


#@app.get("/ej")
#def read_root(request:Request):
#    return {'s':'sd'}
