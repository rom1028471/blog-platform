# backend/app/services/role_service.py
from sqlalchemy.orm import Session
from ..models.role import Role

def get_role_by_name(db: Session, name: str) -> Role | None:
    return db.query(Role).filter(Role.name == name).first()