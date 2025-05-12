# backend/app/initial_data.py
from sqlalchemy.orm import Session
from .models.role import Role
from .models.user import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def init_data(db: Session):
    # Создаем роли, если их нет
    if db.query(Role).count() == 0:
        db.add(Role(name="USER"))
        db.add(Role(name="ADMIN"))
        db.commit()

    # Создаем админа, если его нет
    admin_role = db.query(Role).filter(Role.name == "ADMIN").first()
    if admin_role and not db.query(User).filter(User.username == "admin").first():
        hashed_password = pwd_context.hash("admin")
        admin = User(
            username="admin",
            password=hashed_password,
            name="Administrator",
            email="admin@example.com"
        )
        admin.roles = [admin_role]
        db.add(admin)
        db.commit() 