# backend/app/services/blog_service.py
from uuid import UUID
from sqlalchemy.orm import Session, joinedload
from app.models.blog import Blog
from app.schemas.blog import BlogResponse, UpdateBlogRequest, BlogsResponse
from app.schemas.user import UserSummary

def create_blog(db: Session, user_id: UUID, blog_data: UpdateBlogRequest) -> BlogResponse:
    """
    Создает новый блог для пользователя
    """
    db_blog = Blog(
        title=blog_data.title,
        description=blog_data.description,
        author_id=user_id
    )
    
    db.add(db_blog)
    db.commit()
    db.refresh(db_blog)
    
    # Явно загружаем связанного пользователя
    db_blog = db.query(Blog)\
                .options(joinedload(Blog.author))\
                .filter(Blog.id == db_blog.id)\
                .first()
    
    return BlogResponse(
        id=db_blog.id,
        title=db_blog.title,
        description=db_blog.description,
        author=UserSummary(
            id=db_blog.author.id,
            name=db_blog.author.name,
            username=db_blog.author.username
        )
    )

def get_blogs(db: Session, page: int, size: int) -> BlogsResponse:
    """
    Получает список блогов с пагинацией
    """
    total = db.query(Blog).count()
    blogs = db.query(Blog)\
              .options(joinedload(Blog.author))\
              .offset(page * size)\
              .limit(size)\
              .all()
    
    items = [
        BlogResponse(
            id=blog.id,
            title=blog.title,
            description=blog.description,
            author=UserSummary(
                id=blog.author.id,
                name=blog.author.name,
                username=blog.author.username
            )
        )
        for blog in blogs
    ]
    
    return BlogsResponse(
        items=items,
        total=total,
        page=page,
        size=size
    )

def get_blog_by_id(db: Session, blog_id: UUID) -> BlogResponse | None:
    """
    Получает блог по ID
    """
    blog = db.query(Blog)\
             .options(joinedload(Blog.author))\
             .filter(Blog.id == blog_id)\
             .first()
    
    if not blog:
        return None
    
    return BlogResponse(
        id=blog.id,
        title=blog.title,
        description=blog.description,
        author=UserSummary(
            id=blog.author.id,
            name=blog.author.name,
            username=blog.author.username
        )
    )

def update_blog(db: Session, blog_id: UUID, blog_data: UpdateBlogRequest) -> BlogResponse:
    """
    Обновляет существующий блог
    """
    blog = db.query(Blog)\
             .options(joinedload(Blog.author))\
             .filter(Blog.id == blog_id)\
             .first()
    
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    
    blog.title = blog_data.title
    blog.description = blog_data.description
    
    db.commit()
    db.refresh(blog)
    
    return BlogResponse(
        id=blog.id,
        title=blog.title,
        description=blog.description,
        author=UserSummary(
            id=blog.author.id,
            name=blog.author.name,
            username=blog.author.username
        )
    )

def delete_blog(db: Session, blog_id: UUID) -> bool:
    try:
        blog = db.query(Blog).filter(Blog.id == blog_id).first()
        if not blog:
            return False
        db.delete(blog)
        db.commit()
        return True
    except:
        db.rollback()
        return False