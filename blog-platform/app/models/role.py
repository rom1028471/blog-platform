# backend/app/models/role.py
from sqlalchemy import Column, String, UUID
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base
import uuid

class Role(Base):
    __tablename__ = "roles"

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(50), unique=True)