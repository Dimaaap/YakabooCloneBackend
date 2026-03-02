from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from admin.knowledges.schema import KnowledgeForAdminPageList
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