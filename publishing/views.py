import json

from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import PublishingSchema, PublishingCreate
from core.models import db_helper
from . import crud
from config import redis_client

router = APIRouter(tags=["pubslishing"])


@router.get("/all", response_model=list[PublishingSchema])
async def get_all_publishing(
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    publishing = await crud.get_all_publishing(session)
    return publishing


@router.post("/create")
async def create_publishing(
        publishing: PublishingCreate,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    new_publishing = await crud.create_publishing(session, publishing)
    if new_publishing:
        return new_publishing
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(new_publishing))


@router.delete("/delete/{slug}")
async def delete_publishing(
        slug: str,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    try:
        redis_client.delete("publishing")
        await crud.delete_publishing_by_slug(slug, session)
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}


@router.get("/{slug}", response_model=PublishingSchema)
async def get_publishing_by_slug(
        slug: str, session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.get_publishing_by_slug(slug, session)


@router.get("/first-letter/{letter}", response_model=list[PublishingSchema])
async def get_publishing_by_first_letter(
        letter: str | None,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.get_publishing_by_title_first_letter(letter, session)


@router.get("/search/", response_model=list[PublishingSchema])
async def search_publishing(
        query: str = Query(...),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.get_publishing_by_query(query, session)


@router.get("/{publishing_id}/books")
async def get_all_books_by_publishing(publishing_id: int,
                                      session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    books = await crud.get_all_publishing_books_by_publishing_id(session, publishing_id)
    return books