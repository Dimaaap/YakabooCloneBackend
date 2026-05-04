from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .user import User
    from .notification import Notification


class UserNotification(Base):
    __tablename__ = "user_notification_association"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    notification_id: Mapped[int] = mapped_column(ForeignKey("notifications.id"))

    is_read: Mapped[bool] = mapped_column(Boolean, default=False, server_default="0")

    user: Mapped["User"] = relationship(back_populates="user_notifications")
    notification: Mapped["Notification"] = relationship(back_populates="user_notifications")
