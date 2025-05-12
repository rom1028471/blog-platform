from sqlalchemy import UUID, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
import uuid

class Blog(Base):
    __tablename__ = "blogs"

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(String(500))
    
    # Только один внешний ключ
    author_id: Mapped[UUID] = mapped_column(UUID, ForeignKey("users.id"))

    # Явно указываем связь
    author: Mapped["User"] = relationship("User", back_populates="blogs", foreign_keys=[author_id])
    posts: Mapped[list["Post"]] = relationship("Post", back_populates="blog", cascade="all, delete-orphan")
    