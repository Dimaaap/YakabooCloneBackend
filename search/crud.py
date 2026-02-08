from fastapi import HTTPException, status, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result, or_, func, desc
from sqlalchemy.orm import selectinload, joinedload

import user_history.crud
from core.models import Book, Author, Publishing, BookSeria, BookInfo, UserSearchHistory

SEARCH_RESPONSE_MAX_COUNT = 7

router = APIRouter(prefix="/search", tags=["Search"])


async def search_response(q: str,
                          user_email: str,
                          session: AsyncSession):
    q = q.strip()
    if not q:
        return {
            "books": [],
            "authors": [],
            "publishers": [],
            "series": []
        }

    ts_query = func.plainto_tsquery(q)

    author_full_name = func.concat(Author.first_name, ' ', Author.last_name)

    book_score = (
        func.ts_rank(Book.search_vector, ts_query) * 0.7 + func.similarity(Book.title, q) * 0.3
    )

    books_res = await session.scalars(
        select(Book)
        .join(Book.authors)
        .options(
            selectinload(Book.authors),
            selectinload(Book.images),
            joinedload(Book.book_info)
        )
        .where(
            Book.search_vector.op("@@")(ts_query) |
            (func.similarity(Book.title, q) > 0.25) |
            (Author.search_vector.op("@@")(ts_query)) |
            (func.similarity(author_full_name, q) > 0.25)
        )
        .order_by(desc(book_score))
        .limit(SEARCH_RESPONSE_MAX_COUNT)
    )
    books_list = books_res.unique().all()

    authors_res = await session.scalars(
        select(Author)
        .where(
            Author.search_vector.op("@@")(ts_query) |
            (func.similarity(func.concat(Author.first_name, ' ', Author.last_name), q) > 0.25)
        )
        .order_by(
            desc(func.ts_rank(Author.search_vector, ts_query) +
                 func.similarity(func.concat(Author.first_name, ' ', Author.last_name), q))
        )
        .limit(SEARCH_RESPONSE_MAX_COUNT)
    )

    publishers_res = await session.scalars(
        select(Publishing)
        .where(
            Publishing.search_vector.op("@@")(ts_query) |
            (func.similarity(Publishing.title, q) > 0.25)
        )
        .order_by(
            desc(func.ts_rank(Publishing.search_vector, ts_query) +
                 func.similarity(Publishing.title, q))
        )
        .limit(SEARCH_RESPONSE_MAX_COUNT)
    )

    series = await session.scalars(
        select(BookSeria)
        .where(BookSeria.title.ilike(f"%{q}%"))
        .limit(SEARCH_RESPONSE_MAX_COUNT)
    )

    books_data = []

    for book in books_list:
        author = book.authors[0] if book.authors else None
        image = book.images[0] if book.images else None
        book_info = book.book_info

        books_data.append({
            "id": book.id,
            "title": book.title,
            "code": book_info.code if book_info else None,
            "slug": book.slug,
            "author_first_name": author.first_name if author else None,
            "author_last_name": author.last_name if author else None,
            "price": book.price,
            "promo_price": book.promo_price,
            "image": image.image_url if image else None,
            "format": book_info.format if book_info else None,
            "in_stock": book_info.in_stock
        })

    authors_data = []

    for author in authors_res.unique().all():
        authors_data.append({
            "id": author.id,
            "first_name": author.first_name,
            "last_name": author.last_name,
            "slug": author.slug,
            "image": author.images[0].image_path if author.images else None,
        })

    await user_history.crud.add_term_to_search_history(session, user_email=user_email, term=q)
    also_searched = await also_search_term(q, session)
    return {
        "books": books_data,
        "authors": authors_data,
        "publishers": publishers_res.unique().all(),
        "series": series.unique().all(),
        "also_searched": also_searched
    }


async def also_search_term(
        q: str,
        session: AsyncSession,
        limit: int = 2
):
    q = q.strip()

    statement = (
        select(UserSearchHistory.term,
               func.count(UserSearchHistory.id).label("cnt"),
               func.similarity(UserSearchHistory.term, q).label("sim")
        )
        .where(
            UserSearchHistory.term != q,
            func.similarity(UserSearchHistory.term, q) > 0.3
        )
        .group_by(UserSearchHistory.term)
        .order_by(
            desc("sim"),
            desc("cnt")
        )
        .limit(limit)
    )

    res = await session.execute(statement)
    return [row.term for row in res.all()]