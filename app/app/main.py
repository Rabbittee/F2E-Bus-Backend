import uvicorn
from fastapi import FastAPI

from app.api import router

app = FastAPI()
app.include_router(router)


def start():
    """Launched with `poetry run start` at root level"""
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)