from pydantic import BaseModel, UUID4, Field
from .user import UserSummary
from .pagination import PaginatedResponse

class BlogBase(BaseModel):
    title: str
    description: str

class BlogResponse(BlogBase):
    id: UUID4
    author: UserSummary
    
    
    class Config:
        from_attributes = True

class BlogsResponse(PaginatedResponse[BlogResponse]):
    pass

class UpdateBlogRequest(BaseModel):
    title: str = Field(..., min_length=1, example="Мой блог")
    description: str = Field(..., min_length=1, example="Описание блога")
    
    class Config:
        from_attributes = True