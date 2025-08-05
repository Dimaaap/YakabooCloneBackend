import asyncio

from sqlalchemy import select, Result, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.models import HobbyBrand, db_helper, Hobby
from hobby_brand.schemas import HobbyBrandSchema, HobbyBrandCreate

from data_strorage import HOBBY_BRANDS

async def create_hobby_brand(
        session: AsyncSession,
        brand: HobbyBrandCreate
) -> HobbyBrand:
    new_brand = HobbyBrand(**brand.model_dump())

    if brand.hobbies:
        statement = select(Hobby).where(Hobby.id.in_(brand.hobbies))
        result = await session.execute(statement)
        hobbies = result.scalars().all()

        for hobby in hobbies:
            hobby.brand = new_brand

    session.add(new_brand)
    await session.commit()
    await session.refresh(new_brand)
    return new_brand


async def delete_brand_by_id(session: AsyncSession, brand_id: int):
    statement = delete(HobbyBrand).where(HobbyBrand.id == brand_id)

    try:
        await session.execute(statement)
        await session.commit()
        return True
    except Exception as e:
        print(e)
        return False

async def get_brand_by_slug(session: AsyncSession, brand_slug: str) -> HobbyBrand:
    statement = (select(HobbyBrand)
                 .options(selectinload(HobbyBrand.hobbies))
                 .where(HobbyBrand.slug == brand_slug))
    result: Result = await session.execute(statement)
    brand = result.scalars().first()
    return brand


async def get_brand_by_id(session: AsyncSession, brand_id: int) -> HobbyBrand:
    statement = (select(HobbyBrand)
                 .options(selectinload(HobbyBrand.hobbies))
                 .where(HobbyBrand.id == brand_id))
    result: Result = await session.execute(statement)
    brand = result.scalars().first()
    return brand


async def get_all_brands(session: AsyncSession) -> list[HobbyBrandSchema]:
    statement = select(HobbyBrand).options(selectinload(HobbyBrand.hobbies)).order_by(HobbyBrand.id)
    result: Result = await session.execute(statement)
    brands = result.scalars().all()
    return brands


async def main():
    async with db_helper.session_factory() as session:
        for brand in HOBBY_BRANDS:
            brand = HobbyBrandCreate(**brand)
            await create_hobby_brand(session, brand)


if __name__ == "__main__":
    import sys

    if sys.platform.startswith("win") and sys.version_info >= (3, 8):
        # Windows fix
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())