from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result, or_

from core.models import Book, Author, Publishing, BookSeria
from .schema import SearchResponse

SEARCH_RESPONSE_MAX_COUNT = 7


def get_author_searchable_full_name(first_name: str, last_name: str) -> tuple[str, str]:
    full_name = f"{first_name} {last_name}"
    full_name_without_spaces = full_name.replace(" ", "")
    return full_name, full_name_without_spaces


async def search_response(q: str,
                          session: AsyncSession):
    q_like = f"%{q.lower()}%"

    books = await session.scalars(
        select(Book)
        .where(
            Book.title.ilike(q_like),
        )
        .limit(SEARCH_RESPONSE_MAX_COUNT)
    )

    authors = await session.scalars(
        select(Author)
        .where(or_(
            Author.first_name.ilike(q_like),
            Author.last_name.ilike(q_like),
            get_author_searchable_full_name(Author.first_name, Author.last_name)[0].ilike(q_like),
            get_author_searchable_full_name(Author.first_name, Author.last_name)[1].ilike(q_like)
        ))
        .limit(SEARCH_RESPONSE_MAX_COUNT)
    )

    