import asyncio

from sqlalchemy import select, Result, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.models import BoardGameAge, db_helper, BoardGame
from game_ages.schemas import GameAgeSchema, GameAgeCreate
from data_strorage import BOARD_GAME_AGES


async def create_game_age(
        session: AsyncSession,
        age: GameAgeSchema
) -> BoardGameAge:
    new_age = BoardGameAge(**age.model_dump())

    if age.board_games:
        statement = select(BoardGame).where(BoardGame.code.in_(age.board_games))
        result = await session.execute(statement)
        board_games = result.scalars().all()

        for game in board_games:
            game.ages.append(new_age)
    session.add(new_age)
    await session.commit()
    await session.refresh(new_age)
    return new_age


async def get_all_ages(session: AsyncSession) -> list[GameAgeSchema]:
    statement = select(BoardGameAge).options(selectinload(BoardGameAge.board_games)).order_by(BoardGameAge.id)
    result: Result = await session.execute(statement)
    ages = result.scalars().all()
    return [GameAgeSchema.model_validate(age) for age in ages]


async def get_age_by_slug(age_slug: str, session: AsyncSession) -> BoardGameAge:
    statement = select(BoardGameAge).where(BoardGameAge.slug == age_slug)
    result: Result = await session.execute(statement)
    age = result.scalars().first()
    return age


async def delete_age_by_slug(age_slug: str, session: AsyncSession):
    statement = delete(BoardGameAge).where(BoardGameAge.slug == age_slug)

    try:
        await session.execute(statement)
        await session.commit()
        return True
    except Exception as e:
        print(e)
        return False