# backend/app/api/post_router.py
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from ..schemas.post import CreatePostRequest, PostResponse, PostsResponse, UpdatePostRequest
from ..schemas.user import UserResponse
from ..services.post_service import (
    get_posts, get_post_by_id, create_post, update_post, delete_post
)
from ..dependencies import get_db, get_current_user

router = APIRouter(prefix="/posts")

@router.get("/", response_model=PostsResponse)
async def get_all_posts(
    page: int = Query(0, ge=0),
    size: int = Query(10, ge=1),
    db: Session = Depends(get_db)
):
    return get_posts(db, page=page, size=size)

@router.post("/", response_model=PostResponse, status_code=201)
async def create_post_for_user(
    post_data: CreatePostRequest,  # changed schema
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_post(db, current_user.id, post_data)