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