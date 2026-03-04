from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from admin.author_facts.schema import AuthorFactsForAdminPage, EditAuthorFact
from admin.authors.errors import NotFoundInDbError
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


async def get_author_fact_by_id(session: AsyncSession, fact_id: int) -> AuthorFacts | bool:
    fact = await session.get(AuthorFacts, fact_id)

    if not fact:
        return False
    return fact


async def update_author_fact(session: AsyncSession, fact_id: int, data: EditAuthorFact) -> bool:
    fact = await get_author_fact_by_id(session, fact_id)

    if not fact:
        raise NotFoundInDbError("Author Fact not found")

    update_data = data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(fact, field, value)

    await session.commit()

    return True