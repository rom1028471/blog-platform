# backend/app/services/user_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from uuid import UUID
from ..models.user import User
from ..schemas.user import UpdateUserRequest
from ..exceptions import UserNotFoundException, ResourceNotFoundException

def get_users(db: Session) -> list[User]:
    return db.query(User).all()

def get_user_by_username(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.username == username).first()

def has_user_with_username(db: Session, username: str) -> bool:
    return db.query(User).filter(User.username == username).first() is not None

def has_user_with_email(db: Session, email: str) -> bool:
    return db.query(User).filter(User.email == email).first() is not None

def validate_and_get_user(db: Session, username: str) -> User:
    user = get_user_by_username(db, username)
    if not user:
        raise UserNotFoundException(f"User {username} not found")
    return user

def create_user(db: Session, user_data) -> User:
    if has_user_with_username(db, user_data.username):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists"
        )
    
    new_user = User(**user_data.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def update_user_info(db: Session, username: str, update_data: UpdateUserRequest) -> User:
    user = validate_and_get_user(db, username)
    
    for field, value in update_data.dict(exclude_unset=True).items():
        setattr(user, field, value)
    
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, username: str) -> None:
    user = validate_and_get_user(db, username)
    db.delete(user)
    db.commit()

def update_user(db: Session, user_id: UUID, update_data: UpdateUserRequest) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ResourceNotFoundException("User", "id", str(user_id))
    
    for field, value in update_data.dict(exclude_unset=True).items():
        setattr(user, field, value)
    
    db.commit()
    db.refresh(user)
    return user