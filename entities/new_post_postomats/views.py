import json

from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from .schema import NewPostPostomatCreate, NewPostPostomatSchema
from core.models import db_helper
from . import crud
from config import redis_client

router = APIRouter(tags=["New Post Postomats"])
REDIS_KEY = "new_post_postomats"


@router.get("/all", response_model=list[NewPostPostomatSchema])
async def get_all_new_post_postomats(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    cache_key = "new_post_postomats:all"

    cached = await redis_client.get(cache_key)
    if cached:
        return json.loads(cached)

    postomats = await crud.get_all_new_post_postomats(session)
    data = [NewPostPostomatSchema.model_validate(p).model_dump() for p in postomats]

    await redis_client.set(cache_key, json.dumps(data))
    return data


@router.post("/create")
async def create_new_post_postomat(postomat: NewPostPostomatCreate,
                                   session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    await redis_client.delete("new_post_postomats:all")
    return await crud.create_new_post_postomat(session, postomat)


@router.get("/{postomat_id}")
async def get_new_post_postomat_by_id(postomat_id: int,
                                      session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    key = f"new_post_postomat:{postomat_id}"
    cached = await redis_client.get(key)

    if cached:
        return json.loads(cached)

    postomat = await crud.get_postomat_by_id(postomat_id, session)

    if not postomat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    data = NewPostPostomatSchema.model_validate(postomat).model_dump()
    await redis_client.set(key, json.dumps(data))
    return data


@router.get("/by-city/{city_id}")
async def get_new_post_postomat_by_city_id(city_id: int,
                                           session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    city_key = f"new_post_postomats_by_city:{city_id}"

    cached = await redis_client.get(city_key)
    if cached:
        return json.loads(cached)

    postomats = await crud.get_new_post_postomats_by_city_id(city_id, session)
    data = [NewPostPostomatSchema.model_validate(p).model_dump() for p in postomats]
    await redis_client.set(city_key, json.dumps(data))

    return data
