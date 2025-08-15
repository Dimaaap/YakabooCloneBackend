from typing import TYPE_CHECKING

from sqlalchemy import String, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .hobby_categories import HobbyCategory
    from .hobby import Hobby


class HobbySubCategory(Base):
    __tablename__ = "hobby_subcategories"

    title: Mapped[str] = mapped_column(String(50))
    slug: Mapped[str] = mapped_column(String(55), unique=True)
    images_src: Mapped[list[str]] = mapped_column(JSON, nullable=True)

    category_id: Mapped[int] = mapped_column(ForeignKey("hobby_categories.id"))
    category: Mapped["HobbyCategory"] = relationship("HobbyCategory", back_populates="subcategories")

    hobbies: Mapped[list["Hobby"]] = relationship(
        "Hobby",
        back_populates="subcategory",
        cascade="all, delete-orphan",
    )
