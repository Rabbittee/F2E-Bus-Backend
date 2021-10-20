from fastapi import FastAPI
from api.routes import queries


app = FastAPI()
app.include_router(queries.router)
