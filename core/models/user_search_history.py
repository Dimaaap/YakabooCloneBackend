from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, func, UniqueConstraint, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .user import User


class UserSearchHistory(Base):
    __tablename__ = "user_search_history"
    __table_args__ = (
        UniqueConstraint("user_id", "id", name="uq_user_search_term"),
    )

    term: Mapped[str] = mapped_column(String(255), nullable=False)
    term_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(), server_default=func.now())
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, server_default="1")

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User", back_populates="search_terms")

    def __str__(self):
        return f"{self.__class__.__name__}(term={self.term}, date={self.term_date})"