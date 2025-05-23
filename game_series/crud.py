import asyncio

from sqlalchemy import select, Result, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.models import GameSeries, db_helper, BoardGame
from game_series.schemas import GameSeriaSchema, GameSeriaCreate
from data_strorage import GAME_SERIES


async def create_game_seria(
        session: AsyncSession,
        seria: GameSeriaSchema
) -> GameSeries:
    new_seria = GameSeries(title=seria.title, slug=seria.slug)

    if seria.board_games:
        statement = select(BoardGame).where(BoardGame.id.in_(seria.board_games))
        result = await session.execute(statement)
        board_games = result.scalars().all()

        for game in board_games:
            game.seria = new_seria
    session.add(new_seria)
    await session.commit()
    await session.refresh(new_seria)
    return new_seria


async def get_all_series(session: AsyncSession) -> list[GameSeriaSchema]:
    statement = select(GameSeries).options(selectinload(GameSeries.board_games)).order_by(GameSeries.id)
    result: Result = await session.execute(statement)
    series = result.scalars().all()
    return [GameSeriaSchema.model_validate(seria) for seria in series]


async def delete_seria_by_id(seria_id: int, session: AsyncSession):
    statement = delete(GameSeries).where(GameSeries.id == seria_id)

    try:
        await session.execute(statement)
        await session.commit()
        return True
    except Exception as e:
        print(e)
        return False


async def get_seria_by_slug(seria_slug: str, session: AsyncSession) -> GameSeries:
    statement = select(GameSeries).where(GameSeries.slug == seria_slug)
    result: Result = await session.execute(statement)
    series = result.scalars().first()
    return series


async def get_seria_by_id(seria_id: int, session: AsyncSession) -> GameSeries:
    statement = select(GameSeries).where(GameSeries.id == seria_id)
    result: Result = await session.execute(statement)
    series = result.scalars().first()
    return series


async def main():
    async with db_helper.session_factory() as session:
        for seria in GAME_SERIES:
            seria = GameSeriaCreate(**seria)
            await create_game_seria(session, seria)


if __name__ == "__main__":
    import sys

    if sys.platform.startswith("win") and sys.version_info >= (3, 8):
        # Windows fix
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())