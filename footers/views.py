import json

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import FooterSchema, FooterCreate
from core.models import db_helper
from . import crud
from config import redis_client

router = APIRouter(tags=["footers"])

SIX_DAYS = 24 * 3600 * 6


@router.get("/all", response_model=list[FooterSchema])
async def get_all_footers(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    cached_footers = await redis_client.get("footers")
    if cached_footers:
        return json.loads(cached_footers)

    footers = await crud.get_all_footers(session)
    await redis_client.set("footers", json.dumps([footer.model_dump() for footer in footers]),
                           ex=SIX_DAYS)
    return footers


@router.post("/create")
async def create_footer(footer: FooterCreate,
                        session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    new_footer = await crud.create_footer(session, footer)
    if new_footer:
        await redis_client.delete("footers")
        return new_footer


@router.delete("/{footer_id}")
async def delete_footer_by_id(footer_id: int,
                              session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    deleted_footer = await crud.delete_footer_by_id(footer_id, session)
    if deleted_footer:
        await redis_client.delete("footers")
        return {"message": f"The footer with id {footer_id} has been deleted"}
    else:
        return {"error": deleted_footer}
