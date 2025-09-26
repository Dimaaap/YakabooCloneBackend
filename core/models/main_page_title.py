from datetime import datetime

from sqlalchemy import String, Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class MainPageTitle(Base):
    __tablename__ = 'main_page_titles'

    title: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True, server_default="1")

    created_at: Mapped["datetime"] = mapped_column(DateTime(timezone=True), server_default=func.now(),
                                                   default=datetime.now(), nullable=False)
    updated_at: Mapped["datetime"] = mapped_column(DateTime(timezone=True), server_default=func.now(),
                                                   default=datetime.now(), onupdate=func.now(), nullable=False)

    def __str__(self):
        return f"{ self.__class__.__name__ }: (title={self.title}, active={self.active})"
