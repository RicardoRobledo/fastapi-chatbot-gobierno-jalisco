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

        return Session


    def __new__(cls, *args, **kwargs):
        
        if cls.__client==None:
            cls.__client = cls.__get_connection()

        return cls.__client
    

    @classmethod
    async def get_procedures(cls):
        """
        This method return all procedures

        :return: list of procedures
        """

        procedures = None

        with cls.__client() as session:
            procedures = session.query(Procedure).all()

        return procedures


    @classmethod
    async def get_procedure(cls, procedure:str):
        """
        This method return a procedure

        :return: procedure
        """

        procedure_found = None

        with cls.__client() as session:
            procedure_found = session.query(Procedure).filter_by(name=procedure).first()

        return procedure_found
