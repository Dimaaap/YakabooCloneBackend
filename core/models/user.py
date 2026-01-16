from typing import TYPE_CHECKING, Optional
from datetime import datetime, date
import enum

from sqlalchemy import String, Boolean, Date, DateTime, Integer, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .wishlists import Wishlist
    from .order import Order
    from .cart import Cart
    from .promo_code_usage import PromoCodeUsage
    from .reviews import Review
    from .book import Book
    from .user_seen_books import UserSeenBook
    from .review_reactions import ReviewReaction


class UserStatusEnum(str, enum.Enum):
    READER = "Читач"
    EXPERT = "Знавець"
    ERUDITE = "Ерудит"
    GENIUS = "Геній"


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
    bonuses: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    level: Mapped[UserStatusEnum] = mapped_column(SQLEnum(UserStatusEnum,
                                                          name="user_status_type", create_type=True),
                                                  default=UserStatusEnum.READER,
                                                  server_default=UserStatusEnum.READER.name)

    date_joined: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(), server_default=str(datetime.now()))
    wishlists: Mapped[list["Wishlist"]] = relationship("Wishlist", back_populates="user")
    reviews: Mapped[list["Review"]] = relationship("Review", back_populates="user")
    orders: Mapped[list["Order"]] = relationship("Order", back_populates="user")
    cart: Mapped["Cart"] = relationship("Cart", back_populates="user", uselist=False)
    promo_usage: Mapped["PromoCodeUsage"] = relationship("PromoCodeUsage", back_populates="user")
    seen_books: Mapped[list["UserSeenBook"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    user_seen_books: Mapped[list["Book"]] = relationship(secondary="user_seen_books", viewonly=True)
    review_reactions: Mapped[list["ReviewReaction"]] = relationship(
        "ReviewReaction",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.get_full_name()}, {self.email})"