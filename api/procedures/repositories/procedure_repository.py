from ...desing_patterns.creational_patterns.singleton.database_singleton import DatabaseSingleton


class ProcedureRepository():

    async def get_procedures(self):
        return await DatabaseSingleton.get_procedures()
