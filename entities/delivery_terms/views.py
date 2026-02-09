from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import DeliveryTermSchema, DeliveryTermCreate
from core.models import db_helper
from . import crud

router = APIRouter(tags=["Delivery Terms"])


@router.get("/all", response_model=list[DeliveryTermSchema])
async def get_all_delivery_terms(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    delivery_terms = await crud.get_all_delivery_terms(session)
    return delivery_terms


@router.post("/create")
async def create_delivery_term(delivery_term: DeliveryTermCreate,
                               session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    new_delivery_term = await crud.create_delivery_term(session, delivery_term)
    return new_delivery_term


@router.delete("/{delivery_term_id}")
async def delete_delivery_term_by_id(delivery_term_id: int,
                                     session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    deleted_delivery_term = await crud.delete_delivery_term_by_id(delivery_term_id=delivery_term_id, session=session)
    if deleted_delivery_term:
        return {"message": f"The delivery term with id {delivery_term_id} has been deleted"}
    else:
        return {"error": deleted_delivery_term}


@router.get("/{delivery_term_id}")
async def get_delivery_term_by_id(delivery_term_id: int,
                                  session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    delivery_term = await crud.get_delivery_term_by_id(delivery_term_id, session)
    return delivery_term


@router.get("/{city_id}")
async def get_delivery_term_by_city_id(city_id: int,
                                       session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    delivery_term = await crud.get_delivery_term_by_city_id(city_id, session)
    return delivery_term


@router.get("/{country_id}")
async def get_delivery_term_by_country_id(country_id: int,
                                          session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    delivery_term = await crud.get_delivery_term_by_country_id(country_id, session)
    return delivery_term