from fastapi import APIRouter
from .ask_ds import router as ask_ds_router


router = APIRouter(prefix='/api')

router.include_router(ask_ds_router)