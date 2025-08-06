from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from hobbies.schema import HobbySchema, HobbyCreate
from core.models import db_helper
from . import crud

router = APIRouter(tags=["Hobbies"])


@router.get("/all", response_model=list[HobbySchema])
async def get_all_hobbies(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    hobbies = await crud.get_all_hobbies(session)
    return hobbies


@router.get("/by-slug/{slug}", response_model=HobbySchema)
async def get_hobby_by_slug(
        slug: str,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    hobby = await crud.get_hobby_by_slug(session, slug)
    return hobby



@router.get("/{hobby_id}", response_model=HobbySchema)
async def get_hobby_by_id(
        hobby_id: int,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    hobby = await crud.get_hobby_by_id(session, hobby_id)
    return hobby


@router.delete("/{hobby_id}")
async def delete_hobby(hobby_id: int,
                       session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    success = await crud.delete_hobby_by_id(session, hobby_id)

    if success:
        return {"message": f"The hobby with id {hobby_id} was deleted"}
    else:
        return {"message": f"Deleting failed"}