from fastapi import APIRouter
from fastapi.responses import JSONResponse
from services.deepseek import DeepseekParser
from time import time
from pydantic import BaseModel
from core import prompts


router = APIRouter()


@router.get('/get_prompt')
async def get_prompt(id: int):
    if not id in prompts:
        return JSONResponse(
            "Упссс.... Такого запроса еще не было",
            status_code=404
        )
    
    if prompts[id] == 202:
        return JSONResponse(
            "Еще обрабатываем",
            status_code=202
        )
    
    return JSONResponse(
        prompts[id],
        status_code=200
    )