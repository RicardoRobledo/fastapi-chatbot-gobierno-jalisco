from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api import config
from api.procedures.models.models import Procedure


__author__ = 'Ricardo'
__version__ = '0.1'


class DatabaseSingleton():
    """
    This class manage our connection to a database
    """


    __client = None


    @classmethod
    def __get_connection(self):
        """
        This method create our client
        """

        Session = sessionmaker(bind=create_engine(config.DATABASE_URL, echo=True))

        return Session()


    def __new__(cls, *args, **kwargs):
        
        if cls.__client==None:
            cls.__client = cls.__get_connection()

        return cls.__client
    

    @classmethod
    async def get_procedures(cls):
        """
        This method return all procedures
        """

        procedures = cls.__client.query(Procedure).all()
        cls.__client.commit()
        return procedures


    @classmethod
    async def get_procedure(cls, procedure:str):
        """
        This method return a procedure
        """

        procedure = cls.__client.query(Procedure).filter_by(name=procedure).first()
        cls.__client.commit()
        return procedure
