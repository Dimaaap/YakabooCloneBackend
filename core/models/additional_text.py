from datetime import datetime

from sqlalchemy import Text, Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class AdditionalText(Base):
    __tablename__ = "additional_text"

    text: Mapped[str] = mapped_column(Text, nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True, server_default="1")