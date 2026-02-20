from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from admin.email_subs.schema import EmailSubsForAdminList
from core.models import EmailSubs


async def get_admin_subs_for_admin_page(session: AsyncSession) -> list[EmailSubsForAdminList]:
    statement = (
        select(EmailSubs)
        .order_by(EmailSubs.id)
    )

    result = await session.execute(statement)
    email_subs = result.scalars().all()

    return [
        EmailSubsForAdminList.model_validate(sub)
        for sub in email_subs
    ]