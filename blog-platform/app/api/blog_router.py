# backend/app/api/blog_router.py
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from uuid import UUID
from ..schemas.blog import BlogResponse, BlogsResponse, UpdateBlogRequest
from ..schemas.pagination import PaginatedResponse
from ..schemas.user import UserResponse
from ..services.blog_service import (
    get_blogs, get_blog_by_id, create_blog, update_blog, delete_blog
)
from ..dependencies import get_db, get_current_user

router = APIRouter(prefix="/blogs")

@router.get("/", response_model=BlogsResponse)
async def get_all_blogs(
    page: int = Query(0, ge=0),
    size: int = Query(100, ge=1),
    db: Session = Depends(get_db)
):
    return get_blogs(db, page=page, size=size)

@router.post("/", response_model=BlogResponse, status_code=status.HTTP_201_CREATED)
async def create_blog_for_user(
    blog_data: UpdateBlogRequest,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_blog(db, current_user.id, blog_data)

@router.get("/{blog_id}", response_model=BlogResponse)
async def get_blog(
    blog_id: UUID,
    db: Session = Depends(get_db)
):
    blog = get_blog_by_id(db, blog_id)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    return blog

@router.put("/{blog_id}", response_model=BlogResponse)
async def update_blog_for_user(
    blog_id: UUID,
    blog_data: UpdateBlogRequest,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    updated_blog = update_blog(db, blog_id, blog_data)
    if not updated_blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog not found or you don't have permission"
        )
    return updated_blog

@router.delete("/{blog_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_blog_for_user(
    blog_id: UUID,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Можно добавить проверку, что блог принадлежит текущему пользователю
    success = delete_blog(db, blog_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog not found or you don't have permission"
        )