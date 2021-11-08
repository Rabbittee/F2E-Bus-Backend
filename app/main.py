import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.api import router
from app.models.Base.Error import CustomException, ErrorType

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


@app.exception_handler(CustomException)
async def unicorn_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "type": exc.type,
            "message": exc.msg
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    message = ', '.join(
        [f"{e['loc'][0]}[{e['loc'][1]}]: {e['msg']}" for e in exc.errors()]
    )
    print(exc.errors())
    return JSONResponse(
        status_code=ErrorType.INVALID_PARMETER[1],
        content={
            "type": ErrorType.INVALID_PARMETER.name,
            "message": f'{ErrorType.INVALID_PARMETER[0]} {message}'
        },
    )


def start():
    """Launched with `poetry run start` at root level"""
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
