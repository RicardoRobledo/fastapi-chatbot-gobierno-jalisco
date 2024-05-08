from pydantic import BaseModel


class ResponseProcedure(BaseModel):

    name:str

    class Config:
        from_attributes = True
