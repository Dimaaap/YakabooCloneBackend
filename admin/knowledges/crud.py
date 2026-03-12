from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from admin.authors.errors import NotFoundInDbError
from admin.knowledges.schema import KnowledgeForAdminPageList, EditKnowledge
from core.models import Knowledge


async def get_knowledge_list_for_admin_page(session: AsyncSession) -> list[KnowledgeForAdminPageList]:
    statement = select(Knowledge).order_by(Knowledge.id)
    result = await session.execute(statement)
    knowledge_list = result.scalars().all()

    return [
        KnowledgeForAdminPageList.model_validate(knowledge)
        for knowledge in knowledge_list
    ]


async def get_knowledge_field_data(session: AsyncSession, knowledge_slug: str) -> KnowledgeForAdminPageList:
    statement = (
        select(Knowledge)
        .where(Knowledge.slug == knowledge_slug)
    )

    result = await session.execute(statement)
    knowledge = result.scalars().first()

    if not knowledge:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Knowledge not found"
        )

    return KnowledgeForAdminPageList.model_validate(knowledge)



async def get_knowledge_by_slug(session: AsyncSession, knowledge_slug: str) -> Knowledge | bool:
    statement = select(Knowledge).where(Knowledge.slug == knowledge_slug)
    knowledge_res = await session.execute(statement)
    knowledge = knowledge_res.scalar_one_or_none()

    if not knowledge:
        return False

    return knowledge


async def update_knowledge(session: AsyncSession, knowledge_slug: str, data: EditKnowledge) -> bool:
    knowledge = await get_knowledge_by_slug(session, knowledge_slug)

    if not knowledge:
        raise NotFoundInDbError("Interesting not found")

    update_data = data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(knowledge, field, value)

    await session.commit()
    await session.refresh(knowledge)
    return True