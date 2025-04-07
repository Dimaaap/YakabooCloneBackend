import asyncio

from fastapi import HTTPException, status
from sqlalchemy import select, Result, delete
from sqlalchemy.ext.asyncio import AsyncSession

from banners.schemas import BannerSchema, BannerCreate
from core.models import Banner, db_helper
from data_strorage import BANNERS


async def create_banner(session: AsyncSession, banner: BannerCreate) -> Banner:
    banner = Banner(image_src=banner.image_src, visible=banner.visible, link=banner.link)
    try:
        session.add(banner)
        await session.commit()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return banner


async def get_all_banners(session: AsyncSession) -> list[BannerSchema]:
    statement = select(Banner).order_by(Banner.id).where(Banner.visible)
    result: Result = await session.execute(statement)
    banners = result.scalars().all()
    return [BannerSchema.model_validate(banner) for banner in banners]


async def delete_banner_by_id(banner_id: int, session: AsyncSession):
    statement = delete(Banner).where(Banner.id == banner_id)
    try:
        await session.execute(statement)
        await session.commit()
        return True
    except Exception as e:
        print(e)
        return False


async def main():
    async with db_helper.session_factory() as session:
        for banner in BANNERS:
            banner = BannerCreate(**banner)
            await create_banner(session, banner)


if __name__ == "__main__":
    import sys

    if sys.platform.startswith("win") and sys.version_info >= (3, 8):
        # Windows fix
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())