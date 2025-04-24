import json

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import BannerSchema, BannerCreate
from core.models import db_helper
from . import crud
from config import redis_client

router = APIRouter(tags=["banners"])

SIX_DAYS = 24 * 3600 * 6


@router.get("/all", response_model=list[BannerSchema])
async def get_all_banners(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    cached_banners = await redis_client.get("banners")
    if cached_banners:
        return json.loads(cached_banners)
    banners = await crud.get_all_banners(session)
    await redis_client.set("banners", json.dumps([banner.model_dump() for banner in banners]),
                           ex=SIX_DAYS)
    return banners


@router.post("/create")
async def create_banner(banner: BannerCreate,
                        session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    new_banner = await crud.create_banner(session=session, banner=banner)
    if new_banner:
        await redis_client.delete("banners")
        return new_banner


@router.delete("/{banner_id}")
async def delete_banner_by_id(banner_id: int,
                              session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    deleted_banner = await crud.delete_banner_by_id(banner_id=banner_id, session=session)
    if deleted_banner:
        await redis_client.delete("banners")
        return {"message": f"The banner with id {banner_id} has been deleted"}
    else:
        return {"error": deleted_banner}