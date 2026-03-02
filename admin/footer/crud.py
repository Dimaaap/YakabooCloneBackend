from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from admin.footer.schema import FooterForAdminList
from core.models import Footer


async def get_footers_for_admin_page(session: AsyncSession) -> list[FooterForAdminList]:
    statement = (
        select(Footer)
        .order_by(Footer.id)
    )

    result = await session.execute(statement)
    footers = result.scalars().all()

    return [
        FooterForAdminList.model_validate(footer)
        for footer in footers
    ]


async def get_footer_field_data(session: AsyncSession, footer_id: int) -> FooterForAdminList:
    statement = (
        select(Footer)
        .where(Footer.id == footer_id)
    )

    result = await session.execute(statement)
    footer = result.scalars().first()

    return FooterForAdminList.model_validate(footer)