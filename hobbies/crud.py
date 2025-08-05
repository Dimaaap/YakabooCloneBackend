import asyncio

from fastapi import HTTPException, status
from sqlalchemy import select, Result, delete
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Hobby, db_helper, HobbyImage
from hobbies.schema import HobbySchema, HobbyCreate, HobbyUpdate


async def create_hobby(session: AsyncSession, hobby_data: HobbyCreate ) -> HobbySchema:
    hobby = Hobby(**hobby_data.model_dump(exclude="images"))

    for image_data in hobby_data.images or []:
        image = HobbyImage(image_url=image_data.image_url)
        hobby.images.append(image)

    try:
        session.add(hobby)
        await session.commit()
        await session.refresh(hobby, ["images", "ages", "brand", "seria", "category"])
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return HobbySchema.model_validate(hobby)


async def get_all_hobbies(session: AsyncSession) -> list[HobbySchema]:
    statement = (select(Hobby)
                 .options(
        joinedload(Hobby.brand),
        selectinload(Hobby.ages),
        joinedload(Hobby.seria),
        selectinload(Hobby.images),
        joinedload(Hobby.category)
    ).order_by(Hobby.id))

    result: Result = await session.execute(statement)
    hobbies = result.scalars().all()
    return [HobbySchema.model_validate(hobby) for hobby in hobbies]
