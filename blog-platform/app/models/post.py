# backend/app/models/post.py
from sqlalchemy import Column, String, UUID, ForeignKey, Text, DateTime, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from .base import Base
import uuid

post_tag = Table(
    "posts_tags",
    Base.metadata,
    Column("post_id", UUID, ForeignKey("posts.id")),
    Column("tag_id", UUID, ForeignKey("tags.id"))
)

class Post(Base):
    __tablename__ = "posts"

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(200))
    content: Mapped[str] = mapped_column(Text)
    brief: Mapped[str] = mapped_column(String(300))
    cover_file_id: Mapped[UUID | None] = mapped_column(UUID, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    blog_id: Mapped[UUID] = mapped_column(UUID, ForeignKey("blogs.id"))
    author_id: Mapped[UUID] = mapped_column(UUID, ForeignKey("users.id"))

    blog: Mapped["Blog"] = relationship("Blog", back_populates="posts")
    author: Mapped["User"] = relationship()
    tags: Mapped[list["Tag"]] = relationship(secondary=post_tag)