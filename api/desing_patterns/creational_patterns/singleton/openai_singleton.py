from typing import List

from openai import OpenAI
from openai import AssistantEventHandler

from api import config
from typing_extensions import override


__author__ = 'Ricardo'
__version__ = '0.1'


class OpenAISingleton():


    __client = None


    @classmethod
    def __get_connection(cls):
        """
        This method create our client
        """
        
        client = OpenAI(api_key=config.OPENAI_API_KEY,)

        return client


    def __new__(cls, *args, **kwargs):
        
        if cls.__client==None:
            cls.__client = cls.__get_connection()

        return cls.__client
    

    @classmethod
    async def create_conversation_thread(cls):
        """
        Make up a thread converation
        """

        return cls.__client.beta.threads.create()


    @classmethod
    async def get_conversation_thread(cls, thread_id):
        """
        Get a thread converation

        :param thread: and int that contain our thread identifier
        """

        return cls.__client.beta.threads.messages.list(thread_id)
    

    @classmethod
    async def delete_conversation_thread(cls, thread_id):
        """
        Remove a thread converation

        :param thread: an string being our thread identifier
        """

        cls.__client.beta.threads.delete(thread_id)


    @classmethod
    async def add_message(cls, msg, thread_id):
        """
        Put a message in our conversation thread

        :param msg: string that contain our message
        :param thread: an int that contain our thread identifier
        """

        msg_create = cls.__client.beta.threads.messages.create(
            thread_id=thread_id,
            role='user',
            content=msg,
        )

        return msg_create


    @classmethod
    async def retrieve_message(cls, thread_id):
        """
        Put a message in our conversation thread

        :param thread: and int that contain our thread identifier
        :return: a string that is our response in json
        """

        messages = cls.__client.beta.threads.messages.list(thread_id)
        message = messages.data[0].content[0].text.value

        return message


    @classmethod
    async def run_thread(cls, thread_id):
        """
        Run our thread

        :param thread: and int that contain our thread identifier
        :return: a stream message
        """

        #from openai.types.beta.assistant_stream_event import ThreadMessageDelta

        #cls.__client.beta.threads.runs.create(
        #    thread_id=thread_id,
        #    assistant_id=config.ASSISTANT_ID,
        #    stream=True
        #)
    
        #def my_iterator(msg):
        #    for event in msg:
        #        yield event

        with cls.__client.beta.threads.runs.stream(
            thread_id=thread_id,
            assistant_id=config.ASSISTANT_ID,
            event_handler=EventHandler()
        ) as stream:
            stream.until_done()
            return stream.get_final_messages()


    @classmethod
    async def close_connection(cls, thread_id):
        """
        This method close our client connection and our thread

        :param thread: and int that contain our thread identifier
        """

        cls.__client.beta.threads.delete(thread_id)
        cls.__client = None


class EventHandler(AssistantEventHandler):

    @override
    def on_text_created(self, text) -> None:
        print(f"\nassistant > ", end="", flush=True)


    @override
    def on_text_delta(self, delta, snapshot):
        print(delta.value, end="", flush=True)


    def on_tool_call_created(self, tool_call):
        print(f"\nassistant > {tool_call.type}\n", flush=True)


    def on_tool_call_delta(self, delta, snapshot):

        if delta.type == 'code_interpreter':
        
            if delta.code_interpreter.input:
                print(delta.code_interpreter.input, end="", flush=True)
        
            if delta.code_interpreter.outputs:
        
                print(f"\n\noutput >", flush=True)
        
                for output in delta.code_interpreter.outputs:
                    if output.type == "logs":
                        print(f"\n{output.logs}", flush=True)
