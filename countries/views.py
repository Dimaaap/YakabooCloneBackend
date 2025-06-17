import json

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import CountriesSchema, CountriesCreate
from core.models import db_helper
from . import crud
from config import redis_client

router = APIRouter(tags=["Countries for Delivery"])


@router.get("/all", response_model=list[CountriesSchema])
async def get_all_countries(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    cached_countries = await redis_client.get("countries")
    if cached_countries:
        return json.loads(cached_countries)
    countries = await crud.get_all_countries(session)
    await redis_client.set("countries", json.dumps([country.model_dump() for country in countries]),
                           ex=24 * 3600 * 6)
    return countries


@router.post("/create")
async def create_country(country: CountriesCreate,
                         session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    new_country = await crud.create_country(session=session, country=country)
    if new_country:
        await redis_client.delete("countries")
        return new_country


@router.delete("/{country_id}")
async def delete_country_by_id(country_id: int,
                               session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    deleted_country = await crud.delete_country_by_id(country_id, session)
    if deleted_country:
        await redis_client.delete("countries")
        return {"message": f"The country with id {country_id} has been deleted"}
    else:
        return {"message": deleted_country}