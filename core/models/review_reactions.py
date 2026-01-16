from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Boolean, DateTime, func, UniqueConstraint, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .user import User
    from .reviews import Review


class ReviewReaction(Base):
    __tablename__ = "review_reactions"

    __table_args__ = (
        UniqueConstraint("user_id", "review_id", name="uq_user_review"),
    )

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    review_id: Mapped[int] = mapped_column(ForeignKey("reviews.id"))

    is_like: Mapped[bool] = mapped_column(Boolean, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow,
                                                 server_default=func.now())

    user: Mapped["User"] = relationship(
        "User", back_populates="review_reactions"
    )

    review: Mapped["Review"] = relationship(
        "Review",
        back_populates="reactions"
    )

    def __str__(self):
        return f"Review: (user_id={self.user_id}, review_id={self.review_id} created_at={self.created_at})"
