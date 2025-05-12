# backend/app/services/tag_service.py
from sqlalchemy.orm import Session
from ..models.tag import Tag

def get_tag_by_name(db: Session, name: str) -> Tag | None:
    return db.query(Tag).filter(Tag.name == name).first()