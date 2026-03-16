from fastapi import HTTPException, status
from sqlalchemy import select, update, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from admin.authors.errors import NotFoundInDbError
from admin.authors.schema import AuthorsListForAdmin, AuthorsUpdate, AuthorCreate
from core.models import Author, AuthorImage


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


async def slug_is_in_database(session: AsyncSession, slug: str) -> bool:
    statement = (
        select(Author)
        .where(Author.slug == slug)
    )

    result = await session.execute(statement)
    authors = result.scalars().all()

    if authors:
        return True
    return False


async def get_author_by_id(session: AsyncSession, author_id: int) -> Author | bool:
    author = await session.get(Author, author_id)

    if not author:
        return False
    return author


async def update_author(session: AsyncSession, author_id: int, data: AuthorsUpdate) -> bool:
    author = await get_author_by_id(session, author_id)

    if not author:
        raise NotFoundInDbError("Author not found")

    update_data = data.model_dump(exclude_unset=True)
    images_src = update_data.pop("images_src", None)

    for field, value in update_data.items():
        setattr(author, field, value)

    await session.commit()
    await session.refresh(author)

    if images_src is not None:
        await session.execute(delete(AuthorImage).where(AuthorImage.author_id == author_id))
        for src in images_src:
            session.add(AuthorImage(author_id=author_id, image_path=src))
        await session.commit()
    return True


async def create_author(session: AsyncSession, data: AuthorCreate) -> Author | bool:
    author = Author(
        first_name=data.first_name,
        last_name=data.last_name,
        slug=data.slug,
        date_of_birth=data.date_of_birth,
        is_active=data.is_active,
        description=data.description
    )

    try:
        session.add(author)
        await session.commit()
        await session.refresh(author)

        for src in data.images_src:
            image = AuthorImage(author_id=author.id, image_path=src)
            session.add(image)
        await session.commit()
    except SQLAlchemyError:
        return False
    return author