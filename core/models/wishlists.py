from typing import TYPE_CHECKING

from sqlalchemy import String, Boolean, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .user import User


class Wishlist(Base):
    __table_args__ = (
        PrimaryKeyConstraint("user_id", "title"),
    )

    title: Mapped[str] = mapped_column(String(100))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, server_default="1")

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User", back_populates="wishlists")

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.title}, {self.user.email})"

    def __repr__(self) -> str:
        return str(self)