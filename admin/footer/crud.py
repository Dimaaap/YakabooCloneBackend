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