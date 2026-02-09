from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy import select, Result
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import UserSeenBook, User, Book, Author


async def add_book_to_seen(session: AsyncSession, user_email: str, book_id: int):
    user_res = await session.execute(select(User).where(User.email == user_email))
    user = user_res.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The user with email { user_email } was not found")

    statement = select(UserSeenBook).where(UserSeenBook.book_id == book_id,
                                           UserSeenBook.user_id == user.id)

    result: Result = await session.execute(statement)
    existing = result.scalar_one_or_none()

    if existing:
        return {}

    new_book_view = UserSeenBook(
        user_id=user.id,
        book_id=book_id,
        seen_date=datetime.now()
    )

    session.add(new_book_view)

    await session.commit()
    await session.refresh(new_book_view)
    return new_book_view


async def get_all_user_seen_books(session: AsyncSession, user_email: str):
    user_select = await session.execute(select(User).where(User.email == user_email))
    user = user_select.scalar_one_or_none()

    statement = (select(UserSeenBook)
                 .options(
                    joinedload(UserSeenBook.book).options(
                        selectinload(Book.authors).options(
                            selectinload(Author.images),
                            joinedload(Author.interesting_fact),
                        ),
                        joinedload(Book.publishing),
                        selectinload(Book.wishlists),
                        selectinload(Book.translators),
                        joinedload(Book.literature_period),
                        joinedload(Book.seria),
                        selectinload(Book.images),
                        joinedload(Book.edition_group),
                        selectinload(Book.illustrators),
                        selectinload(Book.reviews),
                    )
                 )
                 .where(UserSeenBook.user_id == user.id)
                 .order_by(UserSeenBook.seen_date.desc()))
    result: Result = await session.execute(statement)
    return result.unique().scalars().all()