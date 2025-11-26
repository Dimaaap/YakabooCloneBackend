import json

from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from .schema import MeestPostOfficeSchema, MeestPostOfficeCreate
from core.models import db_helper
from . import crud
from config import redis_client

router = APIRouter(tags=["Meest Post Offices"])
REDIS_KEY = "meest_post_offices"


@router.get("/all", response_model=list[MeestPostOfficeSchema])
async def get__all_meest_post_offices(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):

    cached_offices = await redis_client.get(REDIS_KEY)

    if cached_offices:
        return json.loads(cached_offices)
    offices = await crud.get_all_meest_offices(session)
    await redis_client.set(REDIS_KEY, json.dumps([office.model_dump() for office in offices], default=str))
    return offices


@router.post("/create")
async def create_meest_post_office(office: MeestPostOfficeCreate,
                                   session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    await redis_client.delete(REDIS_KEY)
    return await crud.create_meest_office(session, office)


@router.get("/{office_id}")
async def get_meest_post_office_by_id(office_id: int,
                                      session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    cached_offices = await redis_client.get(REDIS_KEY)

    if cached_offices:
        offices = json.loads(cached_offices)

        for office in offices:
            if office["id"] == office_id:
                return office
    offices = await crud.get_all_meest_offices(session)
    await redis_client.set(REDIS_KEY, json.dumps([office.model_dump() for office in offices], default=str))
    return await crud.get_office_by_id(office_id, session)


@router.get("/by-city/{city_id}")
async def get_meest_post_offices_by_city_id(city_id: int,
                                            session=Depends(db_helper.scoped_session_dependency)):
    cached_offices = await redis_client.get(REDIS_KEY)

    if cached_offices:
        offices = json.loads(cached_offices)
        res = []
        for office in offices:
            if office["city_id"] == city_id:
                res.append(office)
        return res
    offices = await crud.get_all_meest_offices(session)
    await redis_client.set(REDIS_KEY, json.dumps([office.model_dump() for office in offices], default=str))
    return await crud.get_meest_office_by_city_id(city_id, session)