from datetime import datetime

from sqlalchemy import Text, Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class AdditionalText(Base):
    __tablename__ = "additional_text"

    text: Mapped[str] = mapped_column(Text, nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True, server_default="1")

    created_at: Mapped["datetime"] = mapped_column(DateTime(timezone=True), server_default=func.now(),
                                                   nullable=False)
    updated_at: Mapped["datetime"] = mapped_column(DateTime(timezone=True), server_default=func.now(),
                                                   onupdate=func.now(), nullable=False)

    def __str__(self):
        return f"{self.__class__.__name__}: (text={ self.text }, active={ self.active })"