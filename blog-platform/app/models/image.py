# backend/app/models/image.py
from sqlalchemy import Column, UUID, String, LargeBinary, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from .base import Base
import uuid

class Image(Base):
    __tablename__ = "images"

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100))
    type: Mapped[str] = mapped_column(String(50))
    data: Mapped[bytes] = mapped_column(LargeBinary)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)