from fastapi import HTTPException, status
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from entities.publishing_banners.schema import PublishingBannerSchema, PublishingBannerCreate
from core.models import PublishingBanners


async def create_publishing_banner(session: AsyncSession,
                                   publishing_banner: PublishingBannerCreate) -> PublishingBanners:
    new_banner = PublishingBanners(**publishing_banner.model_dump())

    try:
        session.add(new_banner)
        await session.commit()
        return new_banner
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


async def get_all_publishing_banners(session: AsyncSession) -> list[PublishingBannerSchema]:
    statement = select(PublishingBanners).order_by(PublishingBanners.id)
    result: Result = await session.execute(statement)
    publishing_banners = result.scalars().all()
    return [PublishingBannerSchema.model_validate(banner) for banner in publishing_banners]


async def get_all_banners_by_publishing_id(publishing_id: int, session: AsyncSession) -> PublishingBanners:
    statement = select(PublishingBanners.where(PublishingBanners.publishing_id == publishing_id))
    result: Result = await session.execute(statement)

    banners = result.scalars().all()
    return banners