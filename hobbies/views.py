import json

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.hobby import HobbyTheme
from hobbies.schema import HobbySchema, HobbyCreate
from core.models import db_helper
from . import crud
from config import redis_client

router = APIRouter(tags=["Hobbies"])
REDIS_KEY = "hobby_themes"


@router.get("/all", response_model=list[HobbySchema])
async def get_all_hobbies(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    hobbies = await crud.get_all_hobbies(session)
    return hobbies


@router.get("/all-hobby-themes")
async def get_all_hobby_themes():
    hobby_themes = await redis_client.get(REDIS_KEY)
    if hobby_themes:
        themes = json.loads(hobby_themes)
    else:
        themes = [{"name": theme.name, "value": theme.value} for theme in HobbyTheme]
        await redis_client.set(REDIS_KEY, json.dumps(themes))
    return themes



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