import json

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import CitiesSchema, CitiesCreate
from core.models import db_helper
from . import crud
from config import redis_client

router = APIRouter(tags=["Cities for Delivery"])


@router.get("/all", response_model=list[CitiesSchema])
async def get_all_cities(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    cached_cities = await redis_client.get("cities")
    if cached_cities:
        return json.loads(cached_cities)
    cities = await crud.get_all_cities(session)
    await redis_client.set("cities", json.dumps([city.model_dump() for city in cities]),
                           ex=24 * 3600 * 6)
    return cities


@router.get("/{city_id}")
async def get_city_by_id(city_id: int,
                         session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    cached_city = await redis_client.get("cities")

    if cached_city:
        cities_data = json.loads(cached_city)
        city_data = None
        for city in cities_data:
            if city.get("id") == city_id:
                city_data = city
                break
        if city_data:
            return city_data
    city = await crud.get_city_by_id(city_id, session)
    if city:
        return city
    return {"message": "404 Not Found"}


@router.post("/create")
async def create_city(city: CitiesCreate,
                      session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    new_city = await crud.create_city(session=session, city=city)
    if new_city:
        await redis_client.delete("cities")
        return new_city


@router.delete("/{city_id}")
async def delete_city_by_id(city_id: int,
                            session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    deleted_city = await crud.delete_city_by_id(city_id, session)
    if deleted_city:
        await redis_client.delete("cities")
        return {"message": f"The city with id { city_id } has been deleted"}
    else:
        return {"error": deleted_city}
