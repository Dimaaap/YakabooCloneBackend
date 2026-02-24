from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from admin.promo_codes.schema import PromoCodesAdminList
from core.models import PromoCode


async def get_promo_codes_for_admin_page(session: AsyncSession) -> list[PromoCodesAdminList]:
    statement = (
        select(PromoCode).
        order_by(PromoCode.id)
    )

    result = await session.execute(statement)
    promo_codes = result.scalars().all()

    return [
        PromoCodesAdminList.model_validate(code)
        for code in promo_codes
    ]