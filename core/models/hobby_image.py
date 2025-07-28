from typing import TYPE_CHECKING

from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .hobby import Hobby


class HobbyImage(Base):
    __tablename__ = "hobby_images"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    image_url: Mapped[str] = mapped_column(String(255), server_default="", default="")

    hobby_id: Mapped[int] = mapped_column(ForeignKey("hobbies.id", ondelete="CASCADE"), nullable=False)
    hobby: Mapped["Hobby"] = relationship(back_populates="images")