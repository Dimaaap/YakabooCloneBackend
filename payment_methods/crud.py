from fastapi import HTTPException, status
from sqlalchemy import select, Result, delete
from sqlalchemy.ext.asyncio import AsyncSession

from payment_methods.schema import PaymentMethodCreate, PaymentMethodSchema
from core.models import PaymentMethod, db_helper


async def create_payment_method(session: AsyncSession, payment_method: PaymentMethodCreate) -> PaymentMethod:
    new_payment_method = PaymentMethod(**payment_method.model_dump())

    try:
        session.add(new_payment_method)
        await session.commit()

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return new_payment_method


async def get_all_payment_methods(session: AsyncSession) -> list[PaymentMethodSchema]:
    statement = select(PaymentMethod).order_by(PaymentMethod.id)
    result: Result = await session.execute(statement)
    payment_methods = result.scalars().all()
    return payment_methods


async def get_payment_method_by_id(payment_method_id: int, session: AsyncSession) -> PaymentMethod:
    statement = select(PaymentMethod).where(PaymentMethod.id == payment_method_id)
    result: Result = await session.execute(statement)
    payment_method = result.scalars().first()
    return payment_method


async def get_payment_method_by_city_id(city_id: int, session: AsyncSession) -> PaymentMethod:
    statement = select(PaymentMethod).where(PaymentMethod.city_id == city_id)
    result: Result = await session.execute(statement)
    payment_method = result.scalars().first()
    return payment_method


async def get_payment_method_by_country_id(country_id: int, session: AsyncSession) -> PaymentMethod:
    statement = select(PaymentMethod).where(PaymentMethod.country_id == country_id)
    result: Result = await session.execute(statement)
    payment_method = result.scalars().first()
    return payment_method


async def delete_payment_method_by_id(payment_method_id: int, session: AsyncSession):
    statement = delete(PaymentMethod).where(PaymentMethod.id == payment_method_id)

    try:
        await session.execute(statement)
        await session.commit()
        return True
    except Exception as e:
        return False


