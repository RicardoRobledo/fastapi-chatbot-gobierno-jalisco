from ..repositories.chatbot_repository import ChatbotRepository 


class ChatbotService():


    async def post_user_message(self, message:str, thread_id:str, procedure:str):

        return await ChatbotRepository().post_user_message(message, thread_id, procedure)


    async def create_thread(self):

        return await ChatbotRepository().create_thread()


    async def delete_thread(self, thread_id:str):

        await ChatbotRepository().delete_thread(thread_id)
