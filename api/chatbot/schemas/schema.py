from pydantic import BaseModel


class RequestChatbot(BaseModel):

    msg: str
    thread_id: str
    procedure: str
