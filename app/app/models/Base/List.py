from typing import Generic, TypeVar, List
from pydantic.generics import GenericModel

T = TypeVar("T")


class List(GenericModel, Generic[T]):
    __root__: List[T]

    def from_json(data: str):
        return List.parse_raw(data)
