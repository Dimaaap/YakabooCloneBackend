import json

from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import PublishingSchema, PublishingCreate, SearchQuery
from core.models import db_helper
from . import crud
from config import redis_client

router = APIRouter(tags=["pubslishing"])


@router.get("/all", response_model=list[PublishingSchema])
async def get_all_publishing(
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    cached_publishing = await redis_client.get("publishing")

    if cached_publishing:
        return json.loads(cached_publishing)

    publishing = await crud.get_all_publishing(session)
    await redis_client.set("publishing", json.dumps([pub.model_dump() for pub in publishing]))
    return publishing


@router.post("/create")
async def create_publishing(
        publishing: PublishingCreate,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    new_publishing = await crud.create_publishing(session, publishing)

    if new_publishing:
        await redis_client.delete("publishing")
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
    cached_publishing = await redis_client.get("publishing")
    if cached_publishing:
        publishing_list = json.loads(cached_publishing)
        for pub in publishing_list:
            if pub["slug"] == slug:
                return pub
    else:
        publishing = await crud.get_all_publishing(session)
        await redis_client.set("publishing", json.dumps([pub.model_dump() for pub in publishing]))
        return await crud.get_publishing_by_slug(slug, session)


@router.get("/first-letter/{letter}", response_model=list[PublishingSchema])
async def get_publishing_by_first_letter(
        letter: str,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    cached_publishing = await redis_client.get("publishing")

    if cached_publishing:
        publishing_list = json.loads(cached_publishing)
        res = []
        for pub in publishing_list:
            if pub["title"][0].lower() == letter.lower():
                res.append(pub)
        return res
    else:
        publishing = await crud.get_all_publishing(session)
        await redis_client.set("publishing", json.dumps([pub.model_dump() for pub in publishing]))
        return await crud.get_publishing_by_title_first_letter(letter, session)


@router.get("/search/", response_model=list[PublishingSchema])
async def search_publishing(
        query: str = Query(...),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    cached_publishing = await redis_client.get('publishing')

    if cached_publishing:
        publishing_list = json.loads(cached_publishing)
        res = []
        for pub in publishing_list:
            if query.lower() in pub['title'].lower():
                res.append(pub)
        return res
    else:
        publishing = await crud.get_all_publishing(session)
        await redis_client.set('publishing', json.dumps([pub.model_dump() for pub in publishing]))
        return await crud.get_publishing_by_query(query, session)