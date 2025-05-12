# backend/app/services/auth_service.py
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..models.user import User
from ..schemas.auth import SignUpRequest

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def authenticate_user(db: Session, username: str, password: str) -> User:
    user = db.query(User).filter(User.username == username).first()
    if not user or not pwd_context.verify(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    return user

def register_user(db: Session, user_data: SignUpRequest) -> User:
    if db.query(User).filter(User.username == user_data.username).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already registered"
        )
    
    hashed_password = pwd_context.hash(user_data.password)
    new_user = User(
        username=user_data.username,
        password=hashed_password,
        name=user_data.name,
        email=user_data.email
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user