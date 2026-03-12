from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from admin.authors.errors import NotFoundInDbError
from admin.promo_codes.schema import PromoCodesAdminList, EditPromoCode
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


async def get_promo_codes_field_data(session: AsyncSession, promo_code_id: int) -> PromoCodesAdminList:
    statement = (
        select(PromoCode)
        .where(PromoCode.id == promo_code_id)
    )

    result = await session.execute(statement)
    promo_code = result.scalars().first()

    return PromoCodesAdminList.model_validate(promo_code)



async def get_promo_code_by_id(session: AsyncSession, promo_code_id: int) -> PromoCode | bool:
    promo_code = await session.get(PromoCode, promo_code_id)

    if not promo_code:
        return False

    return promo_code


async def update_promo_code(session: AsyncSession, promo_code_id: int, data: EditPromoCode) -> bool:
    promo_code = await get_promo_code_by_id(session, promo_code_id)

    if not promo_code:
        raise NotFoundInDbError("Promo Code not found")

    update_data = data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(promo_code, field, value)

    await session.commit()
    await session.refresh(promo_code)
    return True