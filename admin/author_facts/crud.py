from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from admin.author_facts.schema import AuthorFactsForAdminPage
from core.models import AuthorFacts


async def get_author_facts_for_admin_page(session: AsyncSession) -> list[AuthorFactsForAdminPage]:
    statement = (
        select(AuthorFacts)
        .options(joinedload(AuthorFacts.author))
        .order_by(AuthorFacts.id)
    )

    result = await session.execute(statement)
    author_facts = result.unique().scalars().all()

    for fact in author_facts:
        fact.author_name = f"{fact.author.first_name} {fact.author.last_name}"

    return [
        AuthorFactsForAdminPage.model_validate(fact)
        for fact in author_facts
    ]


async def get_author_fact_field_data(session: AsyncSession, fact_id: int) -> AuthorFactsForAdminPage:
    statement = (
        select(AuthorFacts)
        .options(joinedload(AuthorFacts.author))
        .where(AuthorFacts.id == fact_id)
    )

    result = await session.execute(statement)
    fact = result.scalars().first()

    fact.author_name = f"{fact.author.first_name} {fact.author.last_name}"
    return AuthorFactsForAdminPage.model_validate(fact)
