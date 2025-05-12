# backend/app/api/user_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..schemas.user import UserResponse, UserSummary
from ..services.user_service import get_users, get_user_by_username, delete_user
from ..dependencies import get_db, admin_required

router = APIRouter(prefix="/users")

@router.get("/", response_model=list[UserResponse])
async def get_all_users(
    db: Session = Depends(get_db),
    current_user = Depends(admin_required)
):
    return get_users(db)

@router.get("/{username}", response_model=UserSummary)
async def get_user(username: str, db: Session = Depends(get_db)):
    user = get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user