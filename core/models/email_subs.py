from datetime import datetime, date

from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class EmailSubs(Base):
    __tablename__ = "email_subs"

    email: Mapped[str] = mapped_column(String(110), unique=True)
    date_sub: Mapped[date] = mapped_column(DateTime(timezone=True), default=datetime.now,
                                           server_default=func.now())

    def __str__(self):
        return f"{self.__class__.__name__}(subscribe_email={self.email})"
