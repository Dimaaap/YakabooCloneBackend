from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from admin.authors.errors import NotFoundInDbError
from admin.banners.schema import BannersListForAdmin, EditBanner
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


async def get_banner_by_id(session: AsyncSession, banner_id: int) -> Banner | bool:
    banner = await session.get(Banner, banner_id)

    if not banner:
        return False
    return banner


async def update_banner(session: AsyncSession, banner_id: int, data: EditBanner) -> bool:
    banner =  await get_banner_by_id(session, banner_id)

    if not banner:
        raise NotFoundInDbError("Banner not found")

    update_data = data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(banner, field, value)

    await session.commit()
    await session.refresh(banner)
    return True