import json

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import InterestingSchema, InterestingCreate
from core.models import db_helper
from . import crud
from config import redis_client

router = APIRouter(tags=["interesting"])

SIX_DAYS = 24 * 3600 * 6


@router.get("/all", response_model=list[InterestingSchema])
async def get_all_interesting(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    cached_interesting = await redis_client.get("interesting")
    if cached_interesting:
        return json.loads(cached_interesting)

    interesting = await crud.get_all_interesting(session)
    await redis_client.set("interesting", json.dumps([interest.model_dump() for interest in interesting]),
                           ex=SIX_DAYS)
    return interesting


@router.post("/create")
async def create_interesting(interesting: InterestingCreate,
                             session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    new_interesting = await crud.create_interesting(session, interesting)
    if new_interesting:
        await redis_client.delete("interesting")
        return new_interesting


@router.delete("/{interesting_id}")
async def delete_interesting_by_id(interesting_id: int,
                                   session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    deleted_interesting = await crud.delete_interesting_by_id(session, interesting_id)
    if deleted_interesting:
        await redis_client.delete("interesting")
        return {"message": f"The interesting with id {interesting_id} has been deleted"}
    else:
        return {"error": deleted_interesting}