import asyncio

from sqlalchemy import select, Result, delete, func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.models import AccessoriesBrand, db_helper, BookAccessories
from accessories_brands.schemas import AccessoryBrandSchema, AccessoryBrandCreate, AccessoryBrandWithCountSchema

from data_strorage import ACCESSORIES_BRANDS

async def create_accessory_brand(
        session: AsyncSession,
        brand: AccessoryBrandCreate
) -> AccessoriesBrand:
    new_brand = AccessoriesBrand(**brand.model_dump())
    
    if brand.accessories:
        statement = select(BookAccessories).where(BookAccessories.id.in_(brand.accessories))
        result: Result = await session.execute(statement)
        accessories = result.scalars().all()
        
        for accessory in accessories:
            accessory.brand = new_brand
    
    session.add(new_brand)
    await session.commit()
    await session.refresh(new_brand)
    return new_brand


async def delete_brand_by_id(session: AsyncSession, brand_id: int):
    statement = delete(AccessoriesBrand).where(AccessoriesBrand.id == brand_id)
    
    try:
        await session.execute(statement)
        await session.commit()
        return True
    except Exception as e:
        return False
    
    
async def get_brand_by_slug(session: AsyncSession, brand_slug: str) -> AccessoriesBrand:
    statement = (select(AccessoriesBrand)
                 .options(selectinload(AccessoriesBrand.accessories))
                 .where(AccessoriesBrand.slug == brand_slug))
    result: Result = await session.execute(statement)
    brand = result.scalars().first()
    return brand 


async def get_brand_by_query(query: str, session: AsyncSession):
    query = query.strip()
    similarity = func.similarity(AccessoriesBrand.title, query)

    statement = (
        select(AccessoriesBrand)
        .where(
            or_(
                similarity >= 0.1,
                AccessoriesBrand.title.like(f"%{query}%"),
            )
        )
        .order_by(similarity)
    )

    result: Result = await session.execute(statement)
    accessory_brands = result.scalars().all()
    return list(accessory_brands) if accessory_brands else []


async def get_all_accessories_by_brand_slug(brand_slug: str, session: AsyncSession):
    statement = (
        select(AccessoriesBrand)
        .where(AccessoriesBrand.slug == brand_slug)
        .options(
            selectinload(AccessoriesBrand.accessories),
            selectinload(AccessoriesBrand.accessories).selectinload(BookAccessories.images)
        )
    )

    result: Result = await session.execute(statement)
    brand = result.scalars().first()
    return brand


async def get_all_brands(session) -> list[AccessoryBrandWithCountSchema]:
    statement = (
        select(
            AccessoriesBrand,
            func.count(BookAccessories.id).label("accessories_count")
        )
        .outerjoin(BookAccessories, BookAccessories.brand_id == AccessoriesBrand.id)
        .group_by(AccessoriesBrand.id)
        .order_by(AccessoriesBrand.title)
    )

    result: Result = await session.execute(statement)
    rows = result.all()

    return [
        AccessoryBrandWithCountSchema(
            brand=AccessoryBrandSchema.model_validate(brand),
            accessory_count = count
        )
        for brand, count in rows
    ]


async def main():
    async with db_helper.session_factory() as session:
        for brand in ACCESSORIES_BRANDS:
            brand = AccessoryBrandCreate(**brand)
            await create_accessory_brand(session, brand)


if __name__ == "__main__":
    import sys

    if sys.platform.startswith("win") and sys.version_info >= (3, 8):
        # Windows fix
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())