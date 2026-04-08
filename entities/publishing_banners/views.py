import json

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from .schema import PublishingBannerSchema, PublishingBannerCreate
from core.models import db_helper
from . import crud
from config import redis_client

router = APIRouter(tags=["Publishing Banners"])

ONE_WEEK = 7 * 24 * 60 * 60


@router.get("/all", response_model=list[PublishingBannerSchema])
async def get_all_publishing_banners(
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):

    cached_banners = await redis_client.get("publishing_banners:all")
    if cached_banners:
        return json.loads(cached_banners)

    publishing_banners = await crud.get_all_publishing_banners(session)
    await redis_client.set("publishing_banners:all", json.dumps([banner.model_dump() for banner in publishing_banners]),
                           ex=ONE_WEEK)
    return publishing_banners


@router.post("/create")
async def create_publishing_banner(banner: PublishingBannerCreate,
                                   session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    new_banner = await crud.create_publishing_banner(session, banner)

    if new_banner:
        await redis_client.delete("publishing_banners:all")
        return new_banner
