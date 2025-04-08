import asyncio

from fastapi import HTTPException, status
from sqlalchemy import select, delete, Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Knowledge, db_helper
from data_strorage import KNOWLEDGES
from knowledges.schemas import KnowledgeSchema


async def create_knowledge(session: AsyncSession, title: str, is_active: bool,
                           slug: str, content: str) -> Knowledge:
    knowledge = Knowledge(title=title, is_active=is_active, slug=slug, content=content)
    try:
        session.add(knowledge)
        await session.commit()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return knowledge


async def get_all_knowledge(session: AsyncSession) -> list[KnowledgeSchema]:
    statement = select(Knowledge).order_by(Knowledge.id).where(Knowledge.is_active)
    result: Result = await session.execute(statement)
    knowledge = result.scalars().all()
    return [KnowledgeSchema.model_validate(kn) for kn in knowledge]


async def get_knowledge_by_slug(session: AsyncSession, slug: str) -> KnowledgeSchema:
    statement = select(Knowledge).where(Knowledge.slug == slug and Knowledge.is_active)
    result: Result = await session.execute(statement)
    knowledge = result.scalars().first()
    return knowledge


async def delete_knowledge_by_slug(slug: str, session: AsyncSession):
    statement = delete(Knowledge).where(Knowledge.slug == slug)
    try:
        await session.execute(statement)
        await session.commit()
        return True
    except Exception as e:
        return False


async def main():
    async with db_helper.session_factory() as session:
        for knowledge in KNOWLEDGES:
            await create_knowledge(session=session,
                                   title=knowledge["title"], slug=knowledge["slug"],
                                   is_active=knowledge.get("is_active", True),
                                   content=knowledge["content"])


if __name__ == "__main__":
    import sys

    if sys.platform.startswith("win") and sys.version_info >= (3, 8):
        # Windows fix
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())
