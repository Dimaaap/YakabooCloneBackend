from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from admin.authors.errors import NotFoundInDbError
from admin.footer.schema import FooterForAdminList, EditFooter, CreateFooter
from core.models import Footer


async def get_footers_for_admin_page(session: AsyncSession) -> list[FooterForAdminList]:
    statement = (
        select(Footer)
        .order_by(Footer.id)
    )

    result = await session.execute(statement)
    footers = result.scalars().all()

    return [
        FooterForAdminList.model_validate(footer)
        for footer in footers
    ]


async def get_footer_field_data(session: AsyncSession, footer_id: int) -> FooterForAdminList:
    statement = (
        select(Footer)
        .where(Footer.id == footer_id)
    )

    result = await session.execute(statement)
    footer = result.scalars().first()

    return FooterForAdminList.model_validate(footer)


async def get_footer_by_id(session: AsyncSession, footer_id: int) -> Footer | bool:
    footer = await session.get(Footer, footer_id)

    if not footer:
        return False

    return footer


async def update_footer(session: AsyncSession, footer_id: int, data: EditFooter) -> bool:
    footer = await get_footer_by_id(session, footer_id)

    if not footer:
        raise NotFoundInDbError("Footer not found")

    update_data = data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(footer, field, value)

    await session.commit()
    await session.refresh(footer)
    return True


async def create_footer(session: AsyncSession, data: CreateFooter) -> Footer | bool:
    footer = Footer(**data.model_dump())

    try:
        session.add(footer)
        await session.commit()
        await session.refresh(footer)
    except SQLAlchemyError:
        return False
    return footer