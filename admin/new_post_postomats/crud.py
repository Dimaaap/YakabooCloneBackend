from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from admin.authors.errors import NotFoundInDbError
from admin.new_post_postomats.schema import NewPostPostomatsForAdmin, EditNewPostPostomat
from core.models import NewPostPostomat


async def get_new_post_postomats_for_admin_page(session: AsyncSession) -> list[NewPostPostomatsForAdmin]:
    statement = (
        select(NewPostPostomat)
        .options(joinedload(NewPostPostomat.city))
        .order_by(NewPostPostomat.id)
    )

    result = await session.execute(statement)
    postomats = result.scalars().all()

    for postomat in postomats:
        postomat.city_title = postomat.city.title

    return [
        NewPostPostomatsForAdmin.model_validate(postomat)
        for postomat in postomats
    ]


async def get_new_post_postomat_field_data(session: AsyncSession, postomat_id: int) -> NewPostPostomatsForAdmin:
    statement = (
        select(NewPostPostomat)
        .options(
            joinedload(NewPostPostomat.city)
        )
        .where(NewPostPostomat.id == postomat_id)
    )

    result = await session.execute(statement)
    postomat = result.scalars().first()
    postomat.city_title = postomat.city.title

    return NewPostPostomatsForAdmin.model_validate(postomat)


async def get_new_post_postomat_by_id(session: AsyncSession, postomat_id: int) -> NewPostPostomat | bool:
    postomat = await session.get(NewPostPostomat, postomat_id)

    if not postomat:
        return False

    return postomat


async def update_new_post_postomat(session: AsyncSession, postomat_id: int, data: EditNewPostPostomat) -> bool:
    postomat = await get_new_post_postomat_by_id(session, postomat_id)

    if not postomat:
        raise NotFoundInDbError("New Post Postomat not found")

    update_data = data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(postomat, field, value)

    await session.commit()
    await session.refresh(postomat)
    return True