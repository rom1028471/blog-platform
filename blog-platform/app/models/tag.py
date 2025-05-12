# backend/app/models/tag.py
from sqlalchemy import Column, String, UUID
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base
import uuid

class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(50), unique=True)