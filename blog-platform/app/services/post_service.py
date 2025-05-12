# backend/app/services/post_service.py
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
import logging
from ..models.post import Post
from ..models.tag import Tag
from ..models.blog import Blog
from ..schemas.post import CreatePostRequest, UpdatePostRequest, PostResponse
from ..schemas.pagination import PaginatedResponse
from ..exceptions import ResourceNotFoundException

logger = logging.getLogger(__name__)

def create_post(db: Session, user_id: UUID, post_data: CreatePostRequest) -> Post:  # changed schema
    # Проверка существования блога
    blog = db.query(Blog).filter(Blog.id == post_data.blog_id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {post_data.blog_id} not found"
        )
    
    # Проверка прав пользователя на блог
    if blog.author_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to create posts in this blog"
        )
    
    # Обработка тегов
    tags = []
    for tag_name in post_data.tags:
        tag_name_clean = tag_name.strip().lower()
        tag = db.query(Tag).filter(func.lower(Tag.name) == tag_name_clean).first()
        if not tag:
            try:
                tag = Tag(name=tag_name_clean)
                db.add(tag)
                db.commit()
                db.refresh(tag)
            except IntegrityError:
                db.rollback()
                tag = db.query(Tag).filter(func.lower(Tag.name) == tag_name_clean).first()
        tags.append(tag)
    
    # Создание поста
    new_post = Post(
        title=post_data.title,
        content=post_data.content,
        brief=post_data.brief,
        cover_file_id=post_data.cover_file_id,
        author_id=user_id,
        blog_id=post_data.blog_id,  # добавлен blog_id
        tags=tags
    )
    
    try:
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
    except Exception as e:
        logger.error(f"Error creating post: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
    
    return new_post

def get_post_by_id(db: Session, post_id: UUID) -> Post:
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise ResourceNotFoundException("Post", "id", str(post_id))
    return post

def update_post(db: Session, post_id: UUID, update_data: UpdatePostRequest) -> Post:
    post = get_post_by_id(db, post_id)
    
    # Обновление тегов
    tags = []
    for tag_name in update_data.tags:
        tag = db.query(Tag).filter(Tag.name == tag_name).first()
        if not tag:
            tag = Tag(name=tag_name)
            db.add(tag)
        tags.append(tag)
    
    post.title = update_data.title
    post.content = update_data.content
    post.brief = update_data.brief
    post.cover_file_id = update_data.cover_file_id
    post.tags = tags
    
    db.commit()
    db.refresh(post)
    return post

def delete_post(db: Session, post_id: UUID) -> None:
    post = get_post_by_id(db, post_id)
    db.delete(post)
    db.commit()

def get_posts(db: Session, page: int = 0, size: int = 100):
    posts = db.query(Post).offset(page * size).limit(size).all()
    total = db.query(Post).count()
    return PaginatedResponse[PostResponse](
        items=posts,
        total=total,
        page=page,
        size=size
    )