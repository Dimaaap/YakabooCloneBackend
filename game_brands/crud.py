import asyncio

from sqlalchemy import select, Result, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.models import BoardGameBrand, db_helper, BoardGame
from game_brands.schemas import GameBrandSchema, GameBrandCreate
from data_strorage import BOARD_GAME_BRANDS


async def create_game_brand(
        session: AsyncSession,
        brand: GameBrandSchema
) -> BoardGameBrand:
    new_brand = BoardGameBrand(**brand.model_dump())

    if brand.board_games:
        statement = select(BoardGame).where(BoardGame.id.in_(brand.board_games))
        result = await session.execute(statement)
        board_games = result.scalars().all()

        for game in board_games:
            game.brand = new_brand
    session.add(new_brand)
    await session.commit()
    await session.refresh(new_brand)
    return new_brand


async def get_all_brands(session: AsyncSession) -> list[GameBrandSchema]:
    statement = select(BoardGameBrand).options(selectinload(BoardGameBrand.board_games)).order_by(BoardGameBrand.id)
    result: Result = await session.execute(statement)
    brands = result.scalars().all()
    return [GameBrandSchema.model_validate(brand) for brand in brands]


async def delete_brand_by_id(brand_id: int, session: AsyncSession):
    statement = delete(BoardGameBrand).where(BoardGameBrand.id == brand_id)

    try:
        await session.execute(statement)
        await session.commit()
        return True
    except Exception as e:
        print(e)
        return False


async def get_brand_by_slug(brand_slug: str, session: AsyncSession) -> BoardGameBrand:
    statement = select(BoardGameBrand).where(BoardGameBrand.slug == brand_slug)
    result: Result = await session.execute(statement)
    brand = result.scalars().first()
    return brand


async def get_brand_by_id(brand_id: int, session: AsyncSession) -> BoardGameBrand:
    statement = (select(BoardGameBrand)
                 .options(selectinload(BoardGameBrand.board_games))
                 .where(BoardGameBrand.id == brand_id))
    result: Result = await session.execute(statement)
    brand = result.scalars().first()
    return brand


async def main():
    async with db_helper.session_factory() as session:
        for brand in BOARD_GAME_BRANDS:
            brand = GameBrandCreate(**brand)
            await create_game_brand(session, brand)


if __name__ == "__main__":
    import sys

    if sys.platform.startswith("win") and sys.version_info >= (3, 8):
        # Windows fix
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())