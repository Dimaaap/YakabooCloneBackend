import asyncio

from fastapi import HTTPException, status
from sqlalchemy import select, Result, delete
from sqlalchemy.ext.asyncio import AsyncSession

from entities.footers.schemas import FooterSchema, FooterCreate
from core.models import Footer, db_helper
from data_strorage import FOOTERS


async def create_footer(session: AsyncSession, footer: FooterCreate) -> Footer:
    footer = Footer(**footer.model_dump())
    try:
        session.add(footer)
        await session.commit()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return footer


async def get_all_footers(session: AsyncSession) -> list[FooterSchema]:
    statement = select(Footer).order_by(Footer.id).where(Footer.active)
    result: Result = await session.execute(statement)
    footers = result.scalars().all()
    return [FooterSchema.model_validate(footer) for footer in footers]


async def delete_footer_by_id(footer_id: int, session: AsyncSession):
    statement = delete(Footer).where(Footer.id == footer_id)
    try:
        await session.execute(statement)
        await session.commit()
        return True
    except Exception as e:
        return False


async def main():
    async with db_helper.session_factory() as session:
        for footer in FOOTERS:
            await create_footer(session, FooterCreate.model_validate(footer))


if __name__ == "__main__":
    import sys

    if sys.platform.startswith("win") and sys.version_info >= (3, 8):
        # Windows fix
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())