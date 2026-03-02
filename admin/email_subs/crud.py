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

async def get_email_sub_field_data(session: AsyncSession, sub_id: int) -> EmailSubsForAdminList:
    statement = (
        select(EmailSubs)
        .where(EmailSubs.id == sub_id)
    )

    result = await session.execute(statement)
    sub = result.scalars().first()
    return EmailSubsForAdminList.model_validate(sub)