# backend/initial_data.py
from sqlalchemy.orm import Session
from .models import Role, User, Blog, Post, Tag
from .database import get_db

def init_data(db: Session):
    if not db.query(Role).first():
        db.add_all([
            Role(name="ROLE_USER"),
            Role(name="ROLE_ADMIN")
        ])
        db.commit()

    admin = db.query(User).filter(User.username == "admin").first()
    if not admin:
        admin = User(
            username="admin",
            password="admin",
            roles=[db.query(Role).filter(Role.name == "ROLE_ADMIN").first()]
        )
        db.add(admin)
        db.commit()

    # Добавление тестовых данных аналогично Java-коду