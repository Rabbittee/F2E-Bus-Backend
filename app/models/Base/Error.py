from enum import Enum


class ErrorType(tuple, Enum):
    RESOURCE_NOT_FOUND = ('Resource not found.', 404)
    INVALID_PARMETER = ('Invalid parameters.', 422)


class CustomException(Exception):
    def __init__(self, error: ErrorType, msg: str = ''):
        self.status_code = error[1]
        self.type = error.name
        self.msg = f"{error[0]}{' ' + msg if msg else ''}"
