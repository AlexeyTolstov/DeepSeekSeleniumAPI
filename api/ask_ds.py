from fastapi import APIRouter
from services.deepseek import DeepseekParser
from time import time
from pydantic import BaseModel


class QueryRequest(BaseModel):
    query: str


router = APIRouter()

@router.post('/ask_ds')
async def ask_ds(request: QueryRequest):
    t = time()
    query = request.query
    print(query)
    ans = DeepseekParser().send(query)
    print(f"🕐 Время: {time() - t}")

    return ans