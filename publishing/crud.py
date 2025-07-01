import asyncio

from fastapi import HTTPException, status
from sqlalchemy import select, Result, func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from publishing.schemas import *
from core.models import Publishing, db_helper
from data_strorage import PUBLISHING


async def create_publishing(session: AsyncSession, publishing: PublishingCreate) -> Publishing:
    new_publishing = Publishing(**publishing.model_dump())

    try:
        session.add(new_publishing)
        await session.commit()
        return new_publishing
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


async def get_all_publishing(session: AsyncSession) -> list[PublishingSchema]:
    statement = select(Publishing).order_by(Publishing.title).where(Publishing.visible)
    result: Result = await session.execute(statement)
    publishing = result.scalars().all()
    return [PublishingSchema.model_validate(pub) for pub in publishing]


async def delete_publishing_by_slug(slug: str, session: AsyncSession):
    statement = select(Publishing).where(Publishing.slug == slug)
    result: Result = await session.execute(statement)
    publishing = result.scalars().first()

    if not publishing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Publishing with slug {slug} was not found")

    await session.delete(publishing)
    await session.commit()


async def get_publishing_by_slug(slug: str, session: AsyncSession) -> Publishing:
    statement = select(Publishing).where(Publishing.slug == slug, Publishing.visible)
    result: Result = await session.execute(statement)
    publishing: Result = result.scalars().first()

    if not publishing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Publishing with slug {slug} was not found")
    return publishing


async def get_publishing_by_title_first_letter(letter: str, session: AsyncSession) -> list[Publishing]:
    statement = select(Publishing).where(Publishing.title.like(f"{letter.upper()}%"), Publishing.visible)
    result: Result = await session.execute(statement)
    publishing = result.scalars().all()
    return list(publishing)


async def get_publishing_by_query(query: str, session: AsyncSession) -> list[Publishing]:
    query = query.strip()
    similarity = func.similarity(Publishing.title, query)
    statement = (select(Publishing)
                 .where(
                    or_(similarity > 0.1,
                        Publishing.title.like(f"%{query}%")))
                 .order_by(similarity.desc()))
    result: Result = await session.execute(statement)
    publishing = result.scalars().all()
    if not publishing:
        return []
    return list(publishing)


async def main():
    async with db_helper.session_factory() as session:
        for pub in PUBLISHING:
            await create_publishing(session, PublishingCreate.model_validate(pub))


if __name__ == "__main__":
    import sys

    if sys.platform.startswith("win") and sys.version_info >= (3, 8):
        # Windows fix
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())


