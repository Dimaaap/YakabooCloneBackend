from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .schema import UkrpostOfficeSchema, UkrpostOfficeCreate
from core.models import db_helper
from . import crud

router = APIRouter(tags=["Ukrpost Offices"])


@router.get("/all", response_model=list[UkrpostOfficeSchema])
async def get_all_ukrpost_offices(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await crud.get_all_ukrpost_offices(session)


@router.post("/create")
async def create_ukrpost_office(office: UkrpostOfficeCreate,
                                session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await crud.create_ukrpost_office(session, office)


@router.delete("/{office_id}")
async def delete_ukrpost_office_by_id(office_id: int,
                                      session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    deleted = await crud.delete_ukrpost_office_by_id(office_id, session)
    if deleted:
        return {"message": f"The ukrpost office with if {office_id} was deleted"}
    return {"error": deleted}


@router.get("/{office_id}")
async def get_ukrpost_office_by_id(office_id: int,
                                   session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    return await crud.get_office_by_id(office_id, session)


@router.get("/by-city/{city_id}")
async def get_ukrpost_offices_by_city_id(city_id: int,
                                         session=Depends(db_helper.scoped_session_dependency)):
    return await crud.get_ukrpost_offices_by_city_id(city_id, session)


