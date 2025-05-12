# backend/app/api/auth_router.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..schemas.auth import AuthResponse, SignUpRequest
from ..schemas.user import UserResponse
from ..services.auth_service import authenticate_user, register_user
from ..dependencies import get_db, create_access_token
from ..models.user import User

router = APIRouter(prefix="/auth")

@router.post("/login", response_model=AuthResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.username})
    return AuthResponse(access_token=access_token, user=user)

@router.post("/signup", response_model=AuthResponse, status_code=201)
async def signup(
    user_data: SignUpRequest,
    db: Session = Depends(get_db)
):
    if db.query(User).filter(User.username == user_data.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    user = register_user(db, user_data)
    access_token = create_access_token(data={"sub": user.username})
    return AuthResponse(access_token=access_token, user=user)