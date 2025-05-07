from typing import TYPE_CHECKING, Optional
from datetime import datetime, date

from sqlalchemy import String, Boolean, Date, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .wishlists import Wishlist


class User(Base):
    first_name: Mapped[str] = mapped_column(String(155), default="", server_default="")
    last_name: Mapped[str] = mapped_column(String(155), default="", server_default="")

    phone_number: Mapped[str] = mapped_column(String(13), unique=True)
    email: Mapped[str] = mapped_column(String(80), unique=True)
    password: Mapped[str] = mapped_column(String(80))
    is_staff: Mapped[bool] = mapped_column(Boolean, default=False, server_default="0")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, server_default="1")
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, server_default="0")
    is_subscribed_to_news: Mapped[bool] = mapped_column(Boolean, default=False, server_default="0")
    birth_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True, default=None, server_default=None)

    date_joined: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(), server_default=str(datetime.now()))
    wishlists: Mapped[list["Wishlist"]] = relationship("Wishlist", back_populates="user")

    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.get_full_name()}, {self.email})"