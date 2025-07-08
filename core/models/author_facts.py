from typing import TYPE_CHECKING

from sqlalchemy import Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .authors import Author


class AuthorFacts(Base):
    __tablename__ = "author_facts"

    fact_text: Mapped[str] = mapped_column(Text, default="", server_default="")

    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"), unique=True)
    author: Mapped["Author"] = relationship("Author", back_populates="interesting_fact")

    def __str__(self):
        return f"{ self.__class__.__name__ }(fact_text={self.fact_text})"