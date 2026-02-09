import json

from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from .schema import NewPostOfficeSchema, NewPostOfficeCreate
from core.models import db_helper
from . import crud
from config import redis_client

router = APIRouter(tags=["New Post Offices"])
REDIS_KEY = "new_post_offices"


@router.get("/all", response_model=list[NewPostOfficeSchema])
async def get_all_new_post_offices(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    cache_key = f"{REDIS_KEY}:all"

    cached = await redis_client.get(cache_key)
    if cached:
        return json.loads(cached)

    offices = await crud.get_all_new_post_offices(session)
    data = [NewPostOfficeSchema.model_validate(office).model_dump() for office in offices]

    await redis_client.set(cache_key, json.dumps(data))
    return data


@router.post("/create")
async def create_new_post_office(office: NewPostOfficeCreate,
                                 session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    await redis_client.delete(f"{REDIS_KEY}:all")
    return await crud.create_new_post_office(session, office)


@router.get("/{office_id}")
async def get_new_post_office_by_id(office_id: int,
                                    session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    key = f"{REDIS_KEY}:{office_id}"
    cached = await redis_client.get(key)

    if cached:
        return json.loads(cached)

    office = await crud.get_office_by_id(office_id, session)

    if not office:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Office not found")

    data = NewPostOfficeSchema.model_validate(office).model_dump()
    await redis_client.set(key, json.dumps(data))
    return data


@router.get("/by-city/{city_id}")
async def get_new_post_office_by_city_id(city_id: int,
                                         session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    city_key = f"new_post_offices_by_city:{city_id}"

    cached = await redis_client.get(city_key)
    if cached:
        return json.loads(cached)

    offices = await crud.get_new_post_office_by_city_id(city_id, session)
    data = [NewPostOfficeSchema.model_validate(p).model_dump() for p in offices]
    await redis_client.set(city_key, json.dumps(data))

    return data