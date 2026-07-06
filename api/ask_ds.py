from fastapi import APIRouter, Response
from services.deepseek import DeepseekParser, deepseek
from time import time
from pydantic import BaseModel


class QueryRequest(BaseModel):
    query: str


router = APIRouter()

@router.post('/ask_ds')
async def ask_ds(request: QueryRequest):
    try:
        t = time()
        query = request.query
        print(query)
        ans = DeepseekParser().send(query)
        print(f"🕐 Время: {time() - t}")

        return Response(
            ans,
            status_code=200
        )
    except:
        return Response(
            "Упссс.... Возникла ошибка",
            status_code=502
        )