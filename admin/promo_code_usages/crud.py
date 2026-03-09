from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from admin.authors.errors import NotFoundInDbError
from admin.promo_code_usages.schema import PromoCodeUsagesForAdmin, EditPromoCodeUsage
from core.models import PromoCodeUsage


async def get_promo_code_usages_for_admin_page(session: AsyncSession) -> list[PromoCodeUsagesForAdmin]:
    statement = (
        select(PromoCodeUsage)
        .options(
            joinedload(PromoCodeUsage.user),
            joinedload(PromoCodeUsage.promo_code)
        )
        .order_by(PromoCodeUsage.id)
    )

    results = await session.execute(statement)
    promo_code_usages = results.scalars().all()

    for usage in promo_code_usages:
        usage.user_email = usage.user.email
        usage.promo_code_title = usage.promo_code.code

    return [
        PromoCodeUsagesForAdmin.model_validate(usage)
        for usage in promo_code_usages
    ]


async def get_promo_code_usages_field_data(session: AsyncSession, usage_id: int) -> PromoCodeUsagesForAdmin:
    statement = (
        select(PromoCodeUsage)
        .options(
            joinedload(PromoCodeUsage.user),
            joinedload(PromoCodeUsage.promo_code)
        )
        .where(PromoCodeUsage.id == usage_id)
    )

    result = await session.execute(statement)
    usage = result.scalars().first()

    usage.user_email = usage.user.email
    usage.promo_code_title = usage.promo_code.code
    return PromoCodeUsagesForAdmin.model_validate(usage)



async def get_promo_code_usage_by_id(session: AsyncSession, usage_id: int) -> PromoCodeUsage | bool:
    usage = await session.get(PromoCodeUsage, usage_id)

    if not usage:
        return False

    return usage


async def update_promo_code_usage(session: AsyncSession, usage_id: int, data: EditPromoCodeUsage) -> bool:
    usage = await get_promo_code_usage_by_id(session, usage_id)

    if not usage:
        raise NotFoundInDbError("Promo Code Usage not found")

    update_data = data.model_dump(exclude_uset=True)

    for field, value in update_data.items():
        setattr(usage, field, value)

    await session.commit()

    return True