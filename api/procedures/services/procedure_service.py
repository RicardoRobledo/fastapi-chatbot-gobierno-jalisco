from ..repositories.procedure_repository import ProcedureRepository


class ProcedureService():

    async def get_procedures(self):
        return await ProcedureRepository().get_procedures()
