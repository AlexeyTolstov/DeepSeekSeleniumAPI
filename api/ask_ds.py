from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from random import randint
from core import add_fast_prompt, add_main_prompt, Prompt


router = APIRouter()

class QueryRequest(BaseModel):
    query: str


@router.post('/ask_fast_ds')
async def ask_fast_ds(request: QueryRequest):
    prompt = Prompt(
        randint(1, 10000000000),
        request.query
    )
    add_fast_prompt(prompt)

    return JSONResponse(
        {"id": prompt.id},
        status_code=202
    )


@router.post('/ask_main_ds')
async def ask_main_ds(request: QueryRequest):
    prompt = Prompt(
        randint(1, 10000000000),
        request.query
    )

    add_main_prompt(prompt)

    return JSONResponse(
        {"id": prompt.id},
        status_code=202
    )