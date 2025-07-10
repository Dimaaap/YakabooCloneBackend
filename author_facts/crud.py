import asyncio

from fastapi import HTTPException, status
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import AuthorFacts, db_helper
from author_facts.schemas import AuthorFactSchema, AuthorFactCreate

from data_strorage import AUTHOR_FACTS


async def create_author_fact(
        session: AsyncSession,
        author_fact: AuthorFactCreate
) -> AuthorFactSchema:
    author_fact = AuthorFacts(**author_fact.model_dump())

    try:
        session.add(author_fact)
        await session.commit()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return author_fact


async def get_all_author_facts(session: AsyncSession) -> list[AuthorFactSchema]:
    statement = select(AuthorFacts).order_by(AuthorFacts.id)
    result: Result = await session.execute(statement)
    author_facts = result.scalars().all()
    return [AuthorFactSchema.model_validate(fact) for fact in author_facts]


async def get_fact_by_author_id(author_id: int, session: AsyncSession) -> AuthorFacts:
    statement = select(AuthorFacts).where(AuthorFacts.author_id == author_id)
    result: Result = await session.execute(statement)
    author_fact = result.scalars().first()
    return author_fact


async def main():
    async with db_helper.session_factory() as session:
        for fact in AUTHOR_FACTS:
            await create_author_fact(session,
                                     AuthorFactCreate.model_validate(fact))


if __name__ == "__main__":
    import sys

    if sys.platform.startswith("win") and sys.version_info >= (3, 8):
        # Windows fix
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())