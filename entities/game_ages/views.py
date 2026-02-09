import json

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import GameAgeSchema, GameAgeCreate
from core.models import db_helper
from . import crud
from config import redis_client
from core.models.board_game_info import BoardLanguages
from core.models.board_games import Type, Kind, PlayersCount

router = APIRouter(tags=["game ages"])

SIX_DAYS = 24 * 36_000 * 6


@router.get("/all", response_model=list[GameAgeSchema])
async def get_all_ages(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    cached_ages = await redis_client.get("game_ages")

    if cached_ages:
        return json.loads(cached_ages)

    game_ages = await crud.get_all_ages(session)
    await redis_client.set("game_ages", json.dumps([age.model_dump() for age in game_ages]))
    return game_ages


@router.get("/languages/all")
async def get_all_languages():
    return [language.value for language in BoardLanguages]


@router.get("/types/all")
async def get_all_game_types():
    return [game_type.value for game_type in Type]


@router.get("/kinds/all")
async def get_all_game_kinds():
    return [kind.value for kind in Kind]


@router.get("/players-count/all")
async def get_all_players_count():
    return [player_count.value for player_count in PlayersCount]


@router.post("/create")
async def create_game_age(age: GameAgeCreate,
                          session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    new_age = await crud.create_game_age(session, age)
    if new_age:
        await redis_client.delete("game_ages")
        return new_age


@router.delete("/{game_age_slug}")
async def delete_game_age_by_slug(game_age_slug: int,
                                  session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    deleted_age = await crud.delete_age_by_slug(game_age_slug, session)
    if deleted_age:
        await redis_client.delete("game_ages")
        return {"message": f"The age with slug {game_age_slug} has been deleted"}
    return {"error": deleted_age}


@router.get("/age_id")
async def get_age_by_id(age_id: int,
                        session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    cached_ages = await redis_client.get("game_ages")
    if cached_ages:
        try:
            ages = json.loads(cached_ages)
            for age in ages:
                if age["id"] == age_id:
                    return GameAgeSchema.model_validate(age)
        except json.JSONDecodeError:
            pass

    age = await crud.get_age_by_id(age_id, session)
    if age is None:
        return {"error": f"No age found with id {age_id}"}

    return GameAgeSchema.model_validate(age)


@router.get("/{age_slug}")
async def get_age_by_slug(age_slug: str,
                          session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    cached_ages = await redis_client.get("game_ages")

    if cached_ages:
        try:
            ages = json.loads(cached_ages)
            for age in ages:
                if age["slug"] == age_slug:
                    return GameAgeSchema.model_validate(age)
        except json.JSONDecodeError:
            pass

    age = await crud.get_age_by_slug(age_slug, session)
    if age is None:
        return {"message": f"No ages found with slug {age_slug}"}
    return GameAgeSchema.model_validate(age)