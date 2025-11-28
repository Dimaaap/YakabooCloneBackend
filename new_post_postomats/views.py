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
    ids_key = "new_post_postomats:ids"

    cached_ids = await redis_client.get(ids_key)

    if cached_ids:
        ids = json.loads(cached_ids)

        postomats = []
        for postomat_id in ids:
            cached = await redis_client.get(f"new_post_postomat:{postomat_id}")
            if cached:
                postomats.append(json.loads(cached))
        return postomats

    postomats = await crud.get_all_new_post_postomats(session)
    ids = [p.id for p in postomats]
    await redis_client.set(ids_key, json.dumps(ids))

    for p in postomats:
        key = f"new_post_postomat:{p.id}"
        await redis_client.set(
            key,
            json.dumps(NewPostPostomatSchema.model_validate(p).model_dump())
        )
    return postomats


@router.post("/create")
async def create_new_post_postomat(postomat: NewPostPostomatCreate,
                                   session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    await redis_client.delete(REDIS_KEY)
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
        ids = json.loads(cached)
        return [json.loads(await redis_client.get(f"new_post_postomat:{id}")) for id in ids]

    postomats = await crud.get_new_post_postomats_by_city_id(city_id, session)
    ids = [p.id for p in postomats]

    await redis_client.set(city_key, json.dumps(ids))

    for p in postomats:
        await redis_client.set(f"new_post_postomat:{p.id}",
                               json.dumps(NewPostPostomatSchema.model_validate(p).model_dump()))
    return postomats
