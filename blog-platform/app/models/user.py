from sqlalchemy import UUID, String, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from .blog import Blog
import uuid

class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    password: Mapped[str] = mapped_column(String)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100), unique=True)
    avatar_file_id: Mapped[UUID | None] = mapped_column(UUID, nullable=True)

    # Связь с блогами
    blogs: Mapped[list["Blog"]] = relationship("Blog", back_populates="author", foreign_keys="Blog.author_id")

# Таблица связи пользователей и ролей
user_role = Table(
    "users_roles",
    Base.metadata,
    Column("user_id", UUID, ForeignKey("users.id", ondelete="CASCADE")),
    Column("role_id", UUID, ForeignKey("roles.id", ondelete="CASCADE"))
)