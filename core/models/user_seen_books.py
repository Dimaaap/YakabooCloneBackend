from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, func, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .user import User
    from .book import Book


class UserSeenBook(Base):
    __tablename__ = "user_seen_books"
    __table_args__ = (
        UniqueConstraint("user_id", "book_id", name="uq_user_book_seen"),
    )

    seen_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(), server_default=func.now())

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User", back_populates="seen_books")

    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))
    book: Mapped["Book"] = relationship("Book", back_populates="seen_by_user")