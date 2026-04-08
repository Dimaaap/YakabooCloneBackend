from typing import TYPE_CHECKING

from sqlalchemy import Text, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .publishing import Publishing


class PublishingBanners(Base):
    __tablename__ = "publishing_banners"

    image_src: Mapped[str] = mapped_column(Text, nullable=False)
    link: Mapped[str] = mapped_column(String, default="", server_default="")

    publishing_id: Mapped[int] = mapped_column(ForeignKey("publishings.id"))
    publishing: Mapped["Publishing"] = relationship("Publishing", back_populates="banners")

    def __str__(self):
        return f"{self.__class__.__name__}(image_src={self.image_src})"