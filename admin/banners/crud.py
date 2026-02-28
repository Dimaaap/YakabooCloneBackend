from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from admin.banners.schema import BannersListForAdmin
from core.models import Banner


async def get_banners_for_admin_page(session: AsyncSession) -> list[BannersListForAdmin]:
    statement = (
        select(Banner)
        .order_by(Banner.id)
    )

    result = await session.execute(statement)
    banners = result.scalars().all()

    return [
        BannersListForAdmin.model_validate(banner)
        for banner in banners
    ]


async def get_banner_field_data(session: AsyncSession, banner_id: int) -> BannersListForAdmin:
    statement = (
        select(Banner)
        .where(Banner.id == banner_id)
    )

    result = await session.execute(statement)
    banner = result.scalars().first()

    return BannersListForAdmin.model_validate(banner)