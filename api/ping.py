from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class QueryRequest(BaseModel):
    query: str


router = APIRouter()

@router.get('/ping')
async def ping():
    return JSONResponse(
        "Все отлично!",
        status_code=200
    )