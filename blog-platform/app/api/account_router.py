# backend/app/api/account_router.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from ..schemas.user import UserResponse, UpdateUserRequest
from ..services.user_service import update_user, delete_user
from ..dependencies import get_db, get_current_user

router = APIRouter(prefix="/account")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@router.get("/me", response_model=UserResponse)
async def get_current_user_endpoint(
    current_user: UserResponse = Depends(get_current_user)
):
    return current_user

@router.put("/me", response_model=UserResponse)
async def update_current_user(
    update_data: UpdateUserRequest,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return update_user(db, current_user.id, update_data)

@router.delete("/me")
async def delete_current_user(
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    delete_user(db, current_user.id)
    return {"message": "Account deleted successfully"}