from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class BooksText(Base):
    __tablename__ = 'books_text'

    text: Mapped[str] = mapped_column(Text, nullable=False)

    def __str__(self):
        return f"{self.__class__.__name__}({self.text})"