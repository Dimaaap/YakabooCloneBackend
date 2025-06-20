import asyncio

from fastapi import HTTPException, status
from sqlalchemy import select, Result, delete
from sqlalchemy.ext.asyncio import AsyncSession

from delivery_terms.schemas import DeliveryTermSchema, DeliveryTermCreate
from core.models import DeliveryTerms, db_helper
from data_strorage import DELIVERY_TERMS


async def create_delivery_term(session: AsyncSession, delivery_term: DeliveryTermCreate) -> DeliveryTerms:
    new_delivery_term = DeliveryTerms(**delivery_term.model_dump())
    try:
        session.add(new_delivery_term)
        await session.commit()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return new_delivery_term


async def get_all_delivery_terms(session: AsyncSession) -> list[DeliveryTermSchema]:
    statement = select(DeliveryTerms).order_by(DeliveryTerms.id)
    result: Result = await session.execute(statement)
    delivery_terms = result.scalars().all()
    return [DeliveryTermSchema.model_validate(term) for term in delivery_terms]


async def get_delivery_term_by_id(delivery_term_id: int, session: AsyncSession) -> DeliveryTerms:
    statement = select(DeliveryTerms).where(DeliveryTerms.id == delivery_term_id).order_by(DeliveryTerms.id)
    result: Result = await session.execute(statement)
    delivery_term = result.scalars().first()
    return delivery_term


async def get_delivery_term_by_city_id(city_id: int, session: AsyncSession) -> DeliveryTerms:
    statement = select(DeliveryTerms).where(DeliveryTerms.city_id == city_id)
    result: Result = await session.execute(statement)
    delivery_term = result.scalars().first()
    return delivery_term


async def get_delivery_term_by_country_id(country_id: int, session: AsyncSession) -> DeliveryTerms:
    statement = select(DeliveryTerms).where(DeliveryTerms.country_id == country_id)
    result: Result = await session.execute(statement)
    delivery_term = result.scalars().first()
    return delivery_term


async def delete_delivery_term_by_id(delivery_term_id: int, session: AsyncSession):
    statement = delete(DeliveryTerms).where(DeliveryTerms.id == delivery_term_id)
    try:
        await session.execute(statement)
        await session.commit()
        return True
    except Exception as e:
        print(e)
        return False


async def main():
    async with db_helper.session_factory() as session:
        for term in DELIVERY_TERMS:
            delivery_term = DeliveryTermCreate(**term)
            await create_delivery_term(session, delivery_term)


if __name__ == "__main__":
    import sys

    if sys.platform.startswith("win") and sys.version_info >= (3, 8):
        # Windows fix
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())

