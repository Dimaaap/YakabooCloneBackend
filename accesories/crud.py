import asyncio

from fastapi import HTTPException, status
from sqlalchemy import select, Result, delete
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import BookAccessories, db_helper, AccessoriesImage, AccessoriesCategory, AccessoriesBrand
from accesories.schemas import AccessoriesSchema, AccessoriesCreate, AccessoriesUpdate
from data_strorage import ACCESSORIES


async def create_accessory(session: AsyncSession, accessory: AccessoriesCreate) -> AccessoriesSchema:
    new_accessory = BookAccessories(**accessory.model_dump(exclude={"images"}))

    for image_data in accessory.images or []:
        image = AccessoriesImage(image_url=image_data.image_url)
        new_accessory.images.append(image)

    try:
        session.add(new_accessory)
        await session.commit()
        statement = (
            select(BookAccessories)
            .where(BookAccessories.id == new_accessory.id)
            .options(
                joinedload(BookAccessories.brand).selectinload(AccessoriesBrand.accessories),
                joinedload(BookAccessories.category).selectinload(AccessoriesCategory.accessories),
                selectinload(BookAccessories.images)
            )
        )

        result = await session.execute(statement)
        new_accessory = result.scalars().first()
    except Exception as exception:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exception))
    return AccessoriesSchema.model_validate(new_accessory)


async def get_all_accessories(session: AsyncSession) -> list[AccessoriesSchema]:
    statement = (
        select(BookAccessories)
        .options(
            joinedload(BookAccessories.brand).selectinload(AccessoriesBrand.accessories),
            joinedload(BookAccessories.category).selectinload(AccessoriesCategory.accessories),
            selectinload(BookAccessories.images)
        ).order_by(BookAccessories.id))

    result: Result = await session.execute(statement)
    accessories = result.scalars().all()
    return [AccessoriesSchema.model_validate(accessory) for accessory in accessories]


async def get_accessory_by_id(session: AsyncSession, accessory_id: int) -> AccessoriesSchema:
    statement = (
        select(BookAccessories)
        .options(
            joinedload(BookAccessories.brand).selectinload(AccessoriesBrand.accessories),
            joinedload(BookAccessories.category).selectinload(AccessoriesCategory.accessories),
            selectinload(BookAccessories.images)
        )
        .where(BookAccessories.id == accessory_id)
    )
    result: Result = await session.execute(statement)
    accessory = result.scalars().first()
    if not accessory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Accessory not found")
    return AccessoriesSchema.model_validate(accessory)


async def get_accessory_by_slug(session: AsyncSession, accessory_slug: str) -> AccessoriesSchema:
    statement = (
        select(BookAccessories)
        .options(
            joinedload(BookAccessories.brand).selectinload(AccessoriesBrand.accessories),
            joinedload(BookAccessories.category).selectinload(AccessoriesCategory.accessories),
            selectinload(BookAccessories.images)
        )
        .where(BookAccessories.slug == accessory_slug)
    )

    result: Result = await session.execute(statement)
    accessory = result.scalars().first()
    if not accessory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Accessory with slug {accessory_slug} not found")
    return AccessoriesSchema.model_validate(accessory)


async def get_all_accessories_by_brand_slug(
        session: AsyncSession, brand_slug: str
) -> list[AccessoriesSchema]:
    statement = (
        select(BookAccessories)
        .join(BookAccessories.brand)
        .options(
            joinedload(BookAccessories.brand).selectinload(AccessoriesBrand.accessories),
            joinedload(BookAccessories.category).selectinload(AccessoriesCategory.accessories),
            selectinload(BookAccessories.images)
        )
        .where(AccessoriesBrand.slug == brand_slug)
        .order_by(BookAccessories.id)
    )

    result: Result = await session.execute(statement)
    accessories = result.scalars().all()

    return accessories if accessories else []


async def update_accessory(session: AsyncSession, accessory_id: int, accessory_data: AccessoriesUpdate):
    accessory = await session.get(BookAccessories, accessory_id)

    if not accessory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Accessory with id {accessory_id} not found")

    for key, value in accessory_data.model_dump(exclude_unset=True).items():
        setattr(accessory, key, value)

    try:
        await session.commit()
        await session.refresh(accessory)

    except Exception as exception:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exception))

    return AccessoriesSchema.model_validate(accessory)


async def delete_accessory_by_id(session: AsyncSession, accessory_id: int) -> bool:
    statement = delete(BookAccessories).where(BookAccessories.id == accessory_id)

    try:
        await session.execute(statement)
        await session.commit()
        return True
    except Exception as exception:
        await session.rollback()
        return False


async def main():
    async with db_helper.session_factory() as session:
        for accessory in ACCESSORIES:
            await create_accessory(session, AccessoriesCreate.model_validate(accessory))


if __name__ == "__main__":
    import sys

    if sys.platform.startswith("win") and sys.version_info >= (3, 8):
        # Windows fix
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())

