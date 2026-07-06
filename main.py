from fastapi import FastAPI
from core import worker_func
from api import router
import threading


app = FastAPI()
app.include_router(router)


@app.on_event("startup")
def startup():
    thread = threading.Thread(target=worker_func, daemon=True)
    thread.start()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='localhost', port=7777)
