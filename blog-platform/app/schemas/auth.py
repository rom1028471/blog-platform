from pydantic import BaseModel, EmailStr
from .user import UserResponse

class LoginRequest(BaseModel):
    username: str
    password: str

class AuthResponse(BaseModel):
    access_token: str
    user: UserResponse

    class Config:
        from_attributes = True

class SignUpRequest(BaseModel):
    username: str
    password: str
    name: str
    email: EmailStr