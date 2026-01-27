import asyncio

from fastapi import HTTPException, status
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import BooksText


async def create_book_text(session: AsyncSession, text: str) -> BooksText | None:
    new_text = BooksText(text=text)

    try:
        session.add(new_text)
        await session.commit()
        return new_text
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


async def get_book_text(session: AsyncSession) -> BooksText:
    books_text = select(BooksText)

    result: Result = await session.execute(books_text)
    text = result.scalars().first()

    if not text:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Text not found")

    return text
