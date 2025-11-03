from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .book import Book
    from .cart import Cart


class CartItem(Base):
    __tablename__ = "cart_items"
    quantity: Mapped[int] = mapped_column(Integer, default=1, server_default="1")
    price: Mapped[int] = mapped_column(Integer, default=0, server_default="0")

    cart_id: Mapped[int] = mapped_column(ForeignKey("carts.id"))
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id", ondelete="CASCADE"))
    book: Mapped["Book"] = relationship("Book", back_populates="cart_items")
    cart: Mapped["Cart"] = relationship("Cart", back_populates="items")

    def __str__(self):
        return f"{self.__class__.__name__}(quantity={self.quantity}, price={self.price})"
