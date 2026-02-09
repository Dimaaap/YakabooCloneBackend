import json

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import GiftSeriaSchema, GiftSeriaCreate
from core.models import db_helper
from . import crud
from config import redis_client

router = APIRouter(tags=["Gift series"])

SIX_DAYS = 24 * 3600 * 6

REDIS_KEY = "gift_series"


@router.get("/all", response_model=list[GiftSeriaSchema])
async def get_all_series(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    cached_series = await redis_client.get(REDIS_KEY)
    if cached_series:
        return json.loads(cached_series)
    game_series = await crud.get_all_series(session)
    await redis_client.set(REDIS_KEY, json.dumps([seria.model_dump() for seria in game_series]),
                           ex=SIX_DAYS)
    return game_series


@router.post("/create")
async def create_game_seria(seria: GiftSeriaCreate,
                            session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    new_seria = await crud.create_gift_seria(session, seria)
    if new_seria:
        await redis_client.delete(REDIS_KEY)
        return new_seria


@router.delete("/{game_seria_id}")
async def delete_game_seria_by_id(seria_id: int,
                                  session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    deleted_seria = await crud.delete_seria_by_id(seria_id, session)
    if deleted_seria:
        await redis_client.delete(REDIS_KEY)
        return {"message": f"The seria with id { seria_id } has been deleted"}
    return {"error": deleted_seria}