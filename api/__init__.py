from .chatbot.controllers.routers import router as chatbot_router
from .procedures.controlles.routers import router as procedures_router

from fastapi import APIRouter


router = APIRouter(prefix='/api/v1')
router.include_router(chatbot_router)
router.include_router(procedures_router)
