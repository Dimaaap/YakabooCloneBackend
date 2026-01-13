from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy import String, Integer, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.book_translators import BookTranslator
from core.models.notebook_subcategories import NotebookSubCategory
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
    from .illustrator_book_association import IllustratorBookAssociation
    from .notebook_categories import NotebookCategory
    from .book_series import BookSeria
    from .book_edition_group import BookEditionGroup
    from .book_illustrators import BookIllustrator
    from .category_book_association import CategoryBookAssociation
    from .categories import Category
    from .double_subcategories import DoubleSubcategory
    from .cart_item import CartItem
    from .double_subcategory_book_association import DoubleSubcategoryBookAssociation
    from .reviews import Review
    from .user_seen_books import UserSeenBook


class Book(Base):
    title: Mapped[str] = mapped_column(String(255), default="", server_default="")
    slug: Mapped[str] = mapped_column(String(255), default="", server_default="")
    price: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    is_top: Mapped[bool] = mapped_column(Boolean, default=False, server_default="0")
    is_promo: Mapped[bool] = mapped_column(Boolean, default=False, server_default="0")
    is_in_chart: Mapped[bool] = mapped_column(Boolean, default=False, server_default="0")
    stars: Mapped[bool] = mapped_column(Integer, default=0, server_default="0")
    promo_price: Mapped[int] = mapped_column(Integer, nullable=True)

    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(), server_default=str(datetime.now()))

    is_notebook: Mapped[bool] = mapped_column(Boolean, default=False, server_default="0")

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

    illustrators: Mapped[list["BookIllustrator"]] = relationship(
        secondary="illustrator_book_association",
        back_populates="book",
        overlaps="illustrator,book",
        lazy="joined"
    )

    seen_by_user: Mapped[list["UserSeenBook"]] = relationship(
        back_populates="book",
        cascade="all, delete-orphan",
        lazy="joined"
    )

    literature_period_id: Mapped[int] = mapped_column(
        ForeignKey("literature_periods.id", name="fk_book_literature_period"),
        nullable=True
    )

    literature_period: Mapped["LiteraturePeriods"] = relationship(
        "LiteraturePeriods", back_populates="books", lazy="joined"
    )

    seria_id: Mapped[int] = mapped_column(
        ForeignKey("book_series.id", name="fk_book_seria"),
        nullable=True
    )

    seria: Mapped["BookSeria"] = relationship(
        "BookSeria", back_populates="books", lazy="joined"
    )

    notebook_category_id: Mapped[int] = mapped_column(
        ForeignKey("notebook_categories.id", name="fk_notebook_category_id"),
        nullable=True
    )

    notebook_category: Mapped["NotebookCategory"] = relationship(
        "NotebookCategory", back_populates="notebooks", lazy="noload"
    )

    notebook_subcategory_id: Mapped[int] = mapped_column(ForeignKey("notebook_subcategories.id"), nullable=True)

    notebook_subcategory: Mapped["NotebookSubCategory"] = relationship("NotebookSubCategory",
                                                                       back_populates="notebooks")

    subcategories: Mapped[list["Subcategory"]] = relationship(
        secondary="subcategory_book_association",
        back_populates="books",
        overlaps="books_details"
    )

    double_subcategories: Mapped[list["DoubleSubcategory"]] = relationship(
        secondary="double_subcategory_book_association",
        back_populates="books",
        overlaps="books_details"
    )

    categories: Mapped[list["Category"]] = relationship(
        "Category",
        secondary="category_book_association",
        back_populates="books",
    )

    publishing_id: Mapped[int] = mapped_column(
        ForeignKey("publishings.id", name="fk_book_publishing")
    )

    edition_group_id: Mapped[int | None] = mapped_column(
        ForeignKey("book_edition_groups.id", name="fk_book_edition_group"),
        nullable=True
    )

    edition_group: Mapped["BookEditionGroup"] = relationship(
        "BookEditionGroup", back_populates="books"
    )

    publishing: Mapped["Publishing"] = relationship("Publishing", back_populates="books", lazy="joined")

    subcategories_details: Mapped[list["SubcategoryBookAssociation"]] = relationship(
        back_populates="book",
        overlaps="books,subcategories"
    )

    double_subcategories_details: Mapped[list["DoubleSubcategoryBookAssociation"]] = relationship(
        back_populates="book",
        overlaps="books,double_subcategories"
    )

    category_details: Mapped[list["CategoryBookAssociation"]] = relationship(
        "CategoryBookAssociation",
        back_populates="book",
        cascade="all, delete-orphan",
        overlaps="categories"
    )

    author_details: Mapped[list["AuthorBookAssociation"]] = relationship(
        back_populates="book",
        overlaps="author,book"
    )

    translator_details: Mapped[list["TranslatorBookAssociation"]] = relationship(
        back_populates="book",
        overlaps="translator,book"
    )

    illustrator_details: Mapped[list["IllustratorBookAssociation"]] = relationship(
        back_populates="book",
        overlaps="illustrator,book"
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

    reviews: Mapped[list["Review"]] = relationship(
        back_populates="book",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    cart_items: Mapped[list["CartItem"]] = relationship(
        "CartItem", back_populates="book", cascade="all, delete-orphan",
    )

    def __str__(self):
        return f"{self.__class__.__name__}(title={self.title}, price={self.price})"