from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .wishlists import Wishlist
    from .book import Book


class WishlistBookAssociation(Base):
    __tablename__ = "wishlist_book_association"

    id: Mapped[int] = mapped_column(primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))
    wishlist_id: Mapped[int] = mapped_column(ForeignKey("wishlists.id"))

    wishlist: Mapped["Wishlist"] = relationship(
        back_populates="book_associations",
        overlaps="books,wishlists"
    )

    book: Mapped["Book"] = relationship(
        back_populates="wishlist_associations",
        overlaps="books,wishlists"
    )