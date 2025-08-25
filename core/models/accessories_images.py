from typing import TYPE_CHECKING
from sqlalchemy import Integer, String, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .book_accessories import BookAccessories


class AccessoriesImage(Base):
    __tablename__ = "accessories_images"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    image_url: Mapped[str] = mapped_column(String(512), default="", server_default="")
    accessory_id: Mapped[int] = mapped_column(ForeignKey("book_accessories.id", ondelete="CASCADE", ),
                                              nullable=False)
    accessory: Mapped["BookAccessories"] = relationship(back_populates="images")

    def __str__(self) -> str:
        return f"{self.__class__.__name__} (image_url={self.image_url})"