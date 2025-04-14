from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .authors import Author


class AuthorImage(Base):
    __tablename__ = "author_images"

    image_path: Mapped[str] = mapped_column(String(255), default="", server_default="")

    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))
    author: Mapped["Author"] = relationship("Author", back_populates="images")

    def __str__(self):
        return f"{self.__class__.__name__}(image_path={self.image_path}, author={self.author.first_name})"