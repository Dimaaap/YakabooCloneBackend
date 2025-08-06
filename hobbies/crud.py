import asyncio

from fastapi import HTTPException, status
from sqlalchemy import select, Result, delete
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Hobby, db_helper, HobbyImage, BoardGameAge, HobbyBrand
from data_strorage import HOBBIES
from hobbies.schema import HobbySchema, HobbyCreate, HobbyUpdate


async def create_hobby(session: AsyncSession, hobby_data: HobbyCreate ) -> HobbySchema:
    hobby = Hobby(**hobby_data.model_dump(exclude={"images", "ages"}))

    for image_data in hobby_data.images or []:
        image = HobbyImage(image_url=image_data.image_url)
        hobby.images.append(image)

    for age_id in hobby_data.ages or []:
        age = await session.get(BoardGameAge, age_id)
        if age:
            hobby.ages.append(age)

    try:
        session.add(hobby)
        await session.commit()
        statement = (
            select(Hobby)
            .where(Hobby.id == hobby.id)
            .options(
                joinedload(Hobby.brand).selectinload(HobbyBrand.hobbies),
                selectinload(Hobby.ages).selectinload(BoardGameAge.board_game),
                joinedload(Hobby.seria),
                selectinload(Hobby.images),
                joinedload(Hobby.category),
            )
        )
        result = await session.execute(statement)
        hobby = result.scalars().first()
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return HobbySchema.model_validate(hobby)


async def get_all_hobbies(session: AsyncSession) -> list[HobbySchema]:
    statement = (select(Hobby)
                 .options(
        joinedload(Hobby.brand).selectinload(HobbyBrand.hobbies),
        selectinload(Hobby.ages).selectinload(BoardGameAge.board_game),
        joinedload(Hobby.seria),
        selectinload(Hobby.images),
        joinedload(Hobby.category)
    ).order_by(Hobby.id))

    result: Result = await session.execute(statement)
    hobbies = result.scalars().all()
    return [HobbySchema.model_validate(hobby) for hobby in hobbies]


async def get_hobby_by_id(session: AsyncSession, hobby_id: int) -> HobbySchema:
    statement = (
        select(Hobby)
        .options(
            joinedload(Hobby.brand).selectinload(HobbyBrand.hobbies),
            selectinload(Hobby.ages).selectinload(BoardGameAge.board_game),
            joinedload(Hobby.seria),
            selectinload(Hobby.images),
            joinedload(Hobby.category)
        )
        .where(Hobby.id == hobby_id)
    )

    result: Result = await session.execute(statement)
    hobby = result.scalars().first()
    if not hobby:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The hobby with id {hobby_id} not found")
    return HobbySchema.model_validate(hobby)


async def get_hobby_by_slug(session: AsyncSession, hobby_slug: str) -> HobbySchema:
    statement = (
        select(Hobby)
        .options(
            joinedload(Hobby.brand).selectinload(HobbyBrand.hobbies),
            selectinload(Hobby.ages).selectinload(BoardGameAge.board_game),
            joinedload(Hobby.seria),
            selectinload(Hobby.images),
            joinedload(Hobby.category)
        )
        .where(Hobby.slug == hobby_slug)
    )

    result: Result = await session.execute(statement)
    hobby = result.scalars().first()
    if not hobby:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The hobby with slug {hobby_slug} not found")
    return HobbySchema.model_validate(hobby)


async def update_hobby(session: AsyncSession, hobby_id: int, hobby_data: HobbyUpdate ) -> HobbySchema:
    hobby = await session.get(Hobby, hobby_id)
    if not hobby:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hobby was not found")

    for key, value in hobby_data.model_dump(exclude_unset=True).items():
        setattr(hobby, key, value)

    try:
        await session.commit()
        await session.refresh(hobby)
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return HobbySchema.model_validate(hobby)


async def delete_hobby_by_id(session: AsyncSession, hobby_id: int) -> bool:
    statement = delete(Hobby).where(Hobby.id == hobby_id)

    try:
        await session.execute(statement)
        await session.commit()
        return True
    except Exception as e:
        await session.rollback()
        return False


async def main():
    async with db_helper.session_factory() as session:
        for hobby in HOBBIES:
            await create_hobby(session, HobbyCreate.model_validate(hobby))


if __name__ == "__main__":
    import sys

    if sys.platform.startswith("win") and sys.version_info >= (3, 8):
        # Windows fix
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())
