from typing import List

from fastapi import APIRouter, Request

from ..services.procedure_service import ProcedureService
from ..schemas.schema import ResponseProcedure


router = APIRouter(prefix='/procedures', tags=['Procedure'])


@router.get('', response_model=List[ResponseProcedure])
async def get_procedures(request:Request):

    procedures = await ProcedureService().get_procedures()
    return [procedure for procedure in procedures]
