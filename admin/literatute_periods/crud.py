from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from admin.literatute_periods.schema import LiteraturePeriodForAdminList
from core.models import LiteraturePeriods


async def get_literature_periods_for_admin_page(session: AsyncSession) -> list[LiteraturePeriodForAdminList]:
    statement = select(LiteraturePeriods).order_by(LiteraturePeriods.id)
    result = await session.execute(statement)
    literature_periods = result.scalars().all()

    return [
        LiteraturePeriodForAdminList.model_validate(period)
        for period in literature_periods
    ]


async def get_literature_period_field_data(session: AsyncSession, literature_period_id: int) -> LiteraturePeriodForAdminList:
    statement = (
        select(LiteraturePeriods)
        .where(LiteraturePeriods.id == literature_period_id)
    )

    result = await session.execute(statement)
    literature_period = result.scalars().first()

    return LiteraturePeriodForAdminList.model_validate(literature_period)