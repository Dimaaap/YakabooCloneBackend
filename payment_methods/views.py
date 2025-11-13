from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .schema import PaymentMethodSchema, PaymentMethodCreate
from core.models import db_helper
from . import crud

router = APIRouter(tags=["Payment Methods"])


@router.get("/all", response_model=list[PaymentMethodSchema])
async def get_all_payment_methods(session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    return await crud.get_all_payment_methods(session)


@router.post("/create")
async def create_payment_method(payment_method: PaymentMethodCreate,
                                session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    return await crud.create_payment_method(session, payment_method)


@router.delete("/{payment_method_id}")
async def delete_payment_method_by_id(payment_method_id: int,
                                      session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    deleted_payment_method = await crud.delete_payment_method_by_id(payment_method_id, session)

    if deleted_payment_method:
        return {"message": f"The payment method with id {payment_method_id} has been deleted"}
    else:
        return {"error": deleted_payment_method}


@router.get("/{payment_method_id}")
async def get_payment_method_by_id(payment_method_id: int,
                                   session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    return await crud.get_payment_method_by_id(payment_method_id, session)


@router.get("/{city_id}")
async def get_payment_method_by_city_id(city_id: int,
                                   session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    payment_method = await crud.get_payment_method_by_city_id(city_id, session)
    return payment_method


@router.get("/{country_id}")
async def get_payment_method_by_country_id(country_id: int,
                                           session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    payment_method = await crud.get_payment_method_by_country_id(country_id, session)
    return payment_method