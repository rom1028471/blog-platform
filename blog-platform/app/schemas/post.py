from pydantic import BaseModel, UUID4
from datetime import datetime
from typing import Set, Optional
from .user import UserSummary
from .tag import TagResponse
from .blog import BlogResponse
from .pagination import PaginatedResponse

class PostBase(BaseModel):
    title: str
    content: str
    brief: str

class PostResponse(PostBase):
    id: UUID4
    cover_file_id: UUID4 | None = None
    created_at: datetime
    author: UserSummary
    tags: Set[TagResponse] = set()
    
    class Config:
        from_attributes = True

class PostsResponse(PaginatedResponse[PostResponse]):
    pass

class PostSummary(BaseModel):
    id: UUID4
    title: str
    brief: str
    cover_file_id: UUID4 | None = None
    created_at: datetime
    author: UserSummary
    tags: list[TagResponse] = []
    
    class Config:
        from_attributes = True

class UpdatePostRequest(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    brief: Optional[str] = None
    cover_file_id: Optional[UUID4] = None
    tags: list[str] = []

class CreatePostRequest(PostBase):
    blog_id: UUID4
    cover_file_id: Optional[UUID4] = None
    tags: list[str] = []