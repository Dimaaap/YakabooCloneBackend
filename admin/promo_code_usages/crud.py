from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from admin.promo_code_usages.schema import PromoCodeUsagesForAdmin
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
