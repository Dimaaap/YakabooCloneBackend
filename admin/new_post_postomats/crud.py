from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from admin.new_post_postomats.schema import NewPostPostomatsForAdmin
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