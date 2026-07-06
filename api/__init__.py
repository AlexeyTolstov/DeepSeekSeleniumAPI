from fastapi import APIRouter
from .ask_ds import router as ask_ds_router
from .get_prompt import router as get_prompt_router
from .ping import router as ping_router


router = APIRouter(prefix='/api')

router.include_router(ping_router)
router.include_router(ask_ds_router)
router.include_router(get_prompt_router)