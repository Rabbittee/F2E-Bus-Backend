import uvicorn
from fastapi import FastAPI

from app.api.routes import queries

app = FastAPI()
app.include_router(queries.router)


def start():
    """Launched with `poetry run start` at root level"""
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)