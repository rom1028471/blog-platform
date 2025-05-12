from pydantic import BaseModel, UUID4
from typing import Optional
from .role import RoleResponse

class UserBase(BaseModel):
    username: str
    email: str

class UserResponse(BaseModel):
    id: UUID4
    username: str
    name: str
    email: str
    blog_id: UUID4 | None = None
    avatar_file_id: UUID4 | None = None
    roles: list[RoleResponse] = []
    
    class Config:
        from_attributes = True

class UpdateUserRequest(BaseModel):
    name: Optional[str] = None
    username: Optional[str] = None
    avatar_file_id: Optional[UUID4] = None

    class Config:
        from_attributes = True  # Автоматическое преобразование ORM-моделей

class UserSummary(BaseModel):
    id: UUID4
    name: str
    username: str
    blog_id: UUID4 | None = None
    avatar_file_id: UUID4 | None = None
    
    class Config:
        from_attributes = True