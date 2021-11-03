import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import router

origins = ["*"]

app = FastAPI()
app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=origins,
    allow_headers=origins,
)


def start():
    """Launched with `poetry run start` at root level"""
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
