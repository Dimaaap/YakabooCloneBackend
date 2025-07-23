from typing import TYPE_CHECKING

from sqlalchemy import String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.book_translators import BookTranslator
from .base import Base

if TYPE_CHECKING:
    from .book_info import BookInfo
    from .author_book_association import AuthorBookAssociation
    from .subcategory_book_association import SubcategoryBookAssociation
    from .wishlist_book_association import WishlistBookAssociation
    from .authors import Author
    from .wishlists import Wishlist
    from .subcategories import Subcategory
    from .publishing import Publishing
    from .book_image import BookImage
    from .literature_periods import LiteraturePeriods
    from .translator_book_association import TranslatorBookAssociation


class Book(Base):
    title: Mapped[str] = mapped_column(String(255), default="", server_default="")
    slug: Mapped[str] = mapped_column(String(255), default="", server_default="")
    price: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    is_top: Mapped[bool] = mapped_column(Boolean, default=False, server_default="0")
    is_promo: Mapped[bool] = mapped_column(Boolean, default=False, server_default="0")
    is_in_chart: Mapped[bool] = mapped_column(Boolean, default=False, server_default="0")
    stars: Mapped[bool] = mapped_column(Integer, default=0, server_default="0")
    promo_price: Mapped[int] = mapped_column(Integer, nullable=True)

    book_info_id: Mapped[int] = mapped_column(
        ForeignKey("book_info.id", name="fk_book_info")
    )

    book_info: Mapped["BookInfo"] = relationship("BookInfo", back_populates="book", lazy="joined")

    authors: Mapped[list["Author"]] = relationship(
        secondary="author_book_association",
        back_populates="book",
        overlaps="author,book",
        lazy="joined"
    )

    translators: Mapped[list["BookTranslator"]] = relationship(
        secondary="translator_book_association",
        back_populates="book",
        overlaps="translator,book",
        lazy="joined"
    )

    literature_period_id: Mapped[int] = mapped_column(
        ForeignKey("literature_periods.id", name="fk_book_literature_period"),
        nullable=True
    )

    literature_period: Mapped["LiteraturePeriods"] = relationship(
        "LiteraturePeriods", back_populates="books", lazy="joined"
    )

    subcategories: Mapped[list["Subcategory"]] = relationship(
        secondary="subcategory_book_association",
        back_populates="books",
        overlaps="books_details"
    )

    publishing_id: Mapped[int] = mapped_column(
        ForeignKey("publishings.id", name="fk_book_publishing")
    )

    publishing: Mapped["Publishing"] = relationship("Publishing", back_populates="books", lazy="joined")

    subcategories_details: Mapped[list["SubcategoryBookAssociation"]] = relationship(
        back_populates="book",
        overlaps="books,subcategories"
    )

    author_details: Mapped[list["AuthorBookAssociation"]] = relationship(
        back_populates="book",
        overlaps="author,book"
    )

    translator_details: Mapped[list["TranslatorBookAssociation"]] = relationship(
        back_populates="book",
        overlaps="translator,book"
    )

    wishlist_associations: Mapped[list["WishlistBookAssociation"]] = relationship(
        back_populates="book",
        overlaps="books"
    )

    wishlists: Mapped[list["Wishlist"]] = relationship(
        secondary="wishlist_book_association",
        back_populates="books",
        overlaps="wishlist_associations",
        lazy="joined"
    )

    images: Mapped[list["BookImage"]] = relationship(
        back_populates="book",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    def __str__(self):
        return f"{self.__class__.__name__}(title={self.title})"