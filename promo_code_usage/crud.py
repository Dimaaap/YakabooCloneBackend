from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import PromoCodeUsage, PromoCode
from promo_codes.crud import validate_promo_code_for_use, increment_promo_code_usage


async def use_promo_code(session: AsyncSession, user_id: int, code: str):
    promo_code = await validate_promo_code_for_use(session, code)

    statement = select(PromoCodeUsage).where(
        PromoCodeUsage.user_id == user_id,
        PromoCodeUsage.promo_id == promo_code.id
    )

    result: Result = await session.execute(statement)
    existing = result.scalar_one_or_none()

    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You`ve already used this promo code")

    usage = PromoCodeUsage(
        user_id=user_id,
        promo_id=promo_code.id,
        used_at=datetime.utcnow()
    )

    session.add(usage)

    await increment_promo_code_usage(session, promo_code)

    await session.commit()
    await session.refresh(usage)
    return usage

async def get_all_promo_usages(session: AsyncSession, user_id: int):
    statement = select(PromoCodeUsage).where(PromoCodeUsage.user_id == user_id)
    result = await session.execute(statement)
    return result.scalars().all()


async def get_usages_by_promo(session: AsyncSession, promo_id: int):
    statement = select(PromoCodeUsage).where(PromoCodeUsage.promo_id == promo_id)
    result = await session.execute(statement)
    return result.scalars().all()