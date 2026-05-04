from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import String, Text, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .notification_user_association import UserNotification


class Notification(Base):
    title: Mapped[str] = mapped_column(String(255), unique=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    image_src: Mapped[str] = mapped_column(String(255), nullable=True)
    link: Mapped[str] = mapped_column(String(255), nullable=True)

    is_global: Mapped[bool] = mapped_column(Boolean, default=True, server_default="1")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                 default=lambda: datetime.now(timezone.utc))
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, server_default="1")

    user_notifications: Mapped[list["UserNotification"]] = relationship(
        back_populates="notification",
        cascade="all, delete-orphan"
    )

    def __str__(self):
        return f"{self.__class__.__name__}(title={self.title}, is_active={self.is_active})"