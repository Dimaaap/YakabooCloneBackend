from fastapi import HTTPException, status, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result, or_

from core.models import Book, Author, Publishing, BookSeria

SEARCH_RESPONSE_MAX_COUNT = 7

router = APIRouter(prefix="/search", tags=["Search"])


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
        ))
        .limit(SEARCH_RESPONSE_MAX_COUNT)
    )

    publishers = await session.scalars(
        select(Publishing)
        .where(Publishing.title.ilike(q_like))
        .limit(SEARCH_RESPONSE_MAX_COUNT)
    )

    series = await session.scalars(
        select(BookSeria)
        .where(BookSeria.title.like(q_like))
        .limit(SEARCH_RESPONSE_MAX_COUNT)
    )

    return {
        "books": books.all(),
        "authors": authors.all(),
        "publishers": publishers.all(),
        "series": series.all(),
    }

    