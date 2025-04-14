import asyncio

from fastapi import HTTPException, status
from sqlalchemy import select, Result, delete
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Author, db_helper, AuthorImage
from authors.schemas import AuthorSchema, AuthorCreate, ImageBase
from data_strorage import AUTHORS, IMAGE_GALLERIES


async def create_author(
        session: AsyncSession,
        author: AuthorCreate
) -> AuthorSchema:
    author = Author(**author.model_dump())
    try:
        session.add(author)
        await session.commit()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return author


async def get_all_authors(session: AsyncSession) -> list[AuthorSchema]:
    statement = select(Author).order_by(Author.id)
    result: Result = await session.execute(statement)
    authors = result.scalars().all()
    return list(authors)


async def create_image_gallery(session: AsyncSession, image: ImageBase) -> AuthorImage:
    author_image = AuthorImage(**image.model_dump())
    session.add(author_image)
    await session.commit()
    return author_image


async def get_all_author_images(session: AsyncSession) -> list[AuthorImage]:
    statement = select(AuthorImage).order_by(AuthorImage.id)
    result: Result = await session.execute(statement)
    author_images = result.scalars().all()
    return list(author_images)


async def get_all_author_images_by_author_id(session: AsyncSession, author_id: int) -> list[AuthorImage]:
    statement = select(AuthorImage).where(AuthorImage.author_id == author_id).order_by(AuthorImage.id)
    result: Result = await session.execute(statement)
    author_images = result.scalars().all()
    return list(author_images)



async def delete_author_by_id(session: AsyncSession, author_id):
    statement = delete(Author).where(Author.id == author_id)
    try:
        await session.execute(statement)
        await session.commit()
        return True
    except Exception as e:
        print(e)
        return False


async def main():
    async with db_helper.session_factory() as session:
        # for author in AUTHORS:
        #     await create_author(session=session,
        #                         author=AuthorCreate.model_validate(author))

        for image in IMAGE_GALLERIES:
            await create_image_gallery(session=session,
                                       image=ImageBase.model_validate(image))


if __name__ == "__main__":
    import sys

    if sys.platform.startswith("win") and sys.version_info >= (3, 8):
        # Windows fix
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())