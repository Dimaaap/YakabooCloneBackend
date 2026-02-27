from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from admin.authors.schema import AuthorsListForAdmin
from core.models import Author


async def get_authors_list_for_admin_page(session: AsyncSession) -> list[AuthorsListForAdmin]:
    statement = (
        select(Author)
        .options(joinedload(Author.interesting_fact),
                 selectinload(Author.images))
        .order_by(Author.id)
    )

    result = await session.execute(statement)
    authors = result.scalars().all()

    for author in authors:
        author.interesting_fact_text = author.interesting_fact.fact_text if author.interesting_fact else None
        author.images_src = [image.image_path for image in author.images] if author.images else []

    return [
        AuthorsListForAdmin.model_validate(author)
        for author in authors
    ]


async def get_author_field_data(session: AsyncSession, author_id: int) -> AuthorsListForAdmin:
    statement = (
        select(Author)
        .options(joinedload(Author.interesting_fact),
                 selectinload(Author.images))
        .where(Author.id == author_id)
    )

    result = await session.execute(statement)
    author = result.scalars().first()

    author.interesting_fact_text = author.interesting_fact.fact_text if author.interesting_fact else None
    author.images_src = [image.image_path for image in author.images] if author.images else []

    return AuthorsListForAdmin.model_validate(author)