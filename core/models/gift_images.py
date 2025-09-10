from typing import TYPE_CHECKING

from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .gifts import Gift


class GiftImage(Base):
    __tablename__ = "gift_images"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    image_url: Mapped[str] = mapped_column(String(255), default="", server_default="")

    gift_id: Mapped[int] = mapped_column(Integer, ForeignKey("gifts.id", ondelete="CASCADE"), nullable=False)
    gift: Mapped["Gift"] = relationship(back_populates="images")