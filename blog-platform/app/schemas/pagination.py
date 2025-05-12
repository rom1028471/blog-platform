from pydantic import BaseModel
from typing import Generic, TypeVar, List

T = TypeVar("T")

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    size: int
    
    @property
    def last(self) -> bool:
        return (self.page + 1) * self.size >= self.total

    class Config:
        from_attributes = True