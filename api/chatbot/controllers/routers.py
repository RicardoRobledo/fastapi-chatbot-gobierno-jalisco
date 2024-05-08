from typing import List

from fastapi.responses import StreamingResponse, JSONResponse
from fastapi import APIRouter, Request

from ..services.chatbot_service import ChatbotService
from ..schemas.schema import RequestChatbot

import json


router = APIRouter(prefix='/chatbot', tags=['Chatbot'])


async def generate_stream_response(msg):
    yield json.dumps({'msg': msg[0].content[0].text.value})


@router.post('/msg')
async def send_message(user_message:RequestChatbot):

    msg = await ChatbotService().post_user_message(user_message.msg, user_message.thread_id, user_message.procedure)

    return StreamingResponse(content=generate_stream_response(msg), media_type="application/json")


@router.get('/thread_id')
async def create_thread(request:Request):

    thread_id = await ChatbotService().create_thread()

    return JSONResponse(content={'thread_id':thread_id.id})


@router.post('/thread_id/{thread_id}')
async def delete_thread(thread_id:str):

    await ChatbotService().delete_thread(thread_id)

    return JSONResponse(content={})
