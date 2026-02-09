import asyncio

from sqlalchemy import select, Result, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.models import BoardGameAge, db_helper, BoardGame
from entities.game_ages.schemas import GameAgeSchema, GameAgeCreate
from data_strorage import BOARD_GAME_AGES


async def create_game_age(
        session: AsyncSession,
        age: GameAgeSchema
) -> BoardGameAge:
    new_age = BoardGameAge(**age.model_dump())

    if age.board_game:
        statement = select(BoardGame).where(BoardGame.code.in_(age.board_game))
        result = await session.execute(statement)
        board_games = result.scalars().all()

        for game in board_games:
            game.ages.append(new_age)
    session.add(new_age)
    await session.commit()
    await session.refresh(new_age)
    return new_age


async def get_all_ages(session: AsyncSession) -> list[GameAgeSchema]:
    statement = select(BoardGameAge).options(selectinload(BoardGameAge.board_game)).order_by(BoardGameAge.id)
    result: Result = await session.execute(statement)
    ages = result.scalars().all()
    return [GameAgeSchema.model_validate(age) for age in ages]


async def delete_age_by_slug(age_slug: str, session: AsyncSession):
    statement = delete(BoardGameAge).where(BoardGameAge.slug == age_slug)

    try:
        await session.execute(statement)
        await session.commit()
        return True
    except Exception as e:
        print(e)
        return False


async def get_age_by_slug(age_slug: str, session: AsyncSession) -> BoardGameAge:
    statement = select(BoardGameAge).where(BoardGameAge.slug == age_slug)
    result: Result = await session.execute(statement)
    age = result.scalars().first()
    return age


async def get_age_by_id(age_id: int, session: AsyncSession) -> BoardGameAge:
    statement = select(BoardGameAge).where(BoardGameAge.id == age_id)
    result: Result = await session.execute(statement)
    age = result.scalars().first()
    return age


async def main():
    async with db_helper.session_factory() as session:
        for age in BOARD_GAME_AGES:
            age = GameAgeCreate(**age)
            await create_game_age(session, age)

if __name__ == "__main__":
    import sys

    if sys.platform.startswith("win") and sys.version_info >= (3, 8):
        # Windows fix
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())