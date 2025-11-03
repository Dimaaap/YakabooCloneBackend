from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .cart_item import CartItem
    from .user import User


class Cart(Base):

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), unique=True)
    user: Mapped["User"] = relationship("User", back_populates="cart")

    items: Mapped[list["CartItem"]] = relationship(
        "CartItem", back_populates="cart", cascade="all, delete-orphan"
    )

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, items={self.items})"