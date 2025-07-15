from typing import TYPE_CHECKING
import enum

from sqlalchemy import Integer, String, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .book import Book


class BookImageType(str, enum.Enum):
    COVER = "cover",
    PAGE = "page"


class BookImage(Base):
    __tablename__ = "book_images"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    image_url: Mapped[str] = mapped_column(String(512), default="", server_default="")
    type: Mapped[BookImageType] = mapped_column(SQLEnum(BookImageType, name="book_image_type_enum"),
                                                default=BookImageType.COVER,
                                                server_default=BookImageType.COVER.name,
                                                nullable=False)

    book_id: Mapped[int] = mapped_column(ForeignKey("books.id", ondelete="CASCADE"), nullable=False)

    book: Mapped["Book"] = relationship(back_populates="images")