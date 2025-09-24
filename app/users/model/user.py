from typing import List

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class User(Base):
    __tablename__: str = "users"

    name: Mapped[str] = mapped_column(String(50), nullable=False)
    lastName: Mapped[str] = mapped_column(String(50), nullable=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[str] = mapped_column(String, nullable=True, default="developer")
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    posts: Mapped[List["Post"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    comments: Mapped[List["Comment"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
