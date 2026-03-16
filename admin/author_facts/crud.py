from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from admin.author_facts.schema import AuthorFactsForAdminPage, EditAuthorFact, CreateAuthorFact
from admin.authors.crud import get_authors_list_for_admin_page
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
    await session.refresh(fact)
    return True


async def create_author_fact(session: AsyncSession, data: CreateAuthorFact) -> AuthorFacts | bool:
    fact = AuthorFacts(**data.model_dump())

    try:
        session.add(fact)
        await session.commit()
        await session.refresh(fact)
    except SQLAlchemyError:
        return False
    return fact


async def set_author_in_choices(session: AsyncSession, form):
    authors = await get_authors_list_for_admin_page(session)
    choices = [(author.id, f"{author.first_name} {author.last_name}") for author in authors]
    form.author_id.choices = choices