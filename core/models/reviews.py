from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy import String, Boolean, Text, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .user import User
    from .book import Book


class Review(Base):
    rate: Mapped[int] = mapped_column(Integer, default=5, server_default="5")
    title: Mapped[str] = mapped_column(String(255), nullable=True)
    comment: Mapped[str] = mapped_column(Text, nullable=False)
    user_name: Mapped[str] = mapped_column(String(255), nullable=False)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(), server_default=str(datetime.now()))
    is_validated: Mapped[bool] = mapped_column(Boolean, default=True, server_default="1")

    user_email: Mapped[str] = mapped_column(ForeignKey("users.email"), nullable=True)
    user: Mapped["User"] = relationship("User", back_populates="reviews")
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))
    book: Mapped["Book"] = relationship("Book", back_populates="reviews")

    def __str__(self) -> str:
        return f"{self.__class__.__name__} (title={self.title} created date={self.created_date})"