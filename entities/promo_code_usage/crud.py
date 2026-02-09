from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import PromoCodeUsage, User
from entities.promo_codes.crud import validate_promo_code_for_use, increment_promo_code_usage


async def use_promo_code(session: AsyncSession, user_email: str, code: str):
    promo_code = await validate_promo_code_for_use(session, code)

    user_res = await session.execute(select(User).where(User.email == user_email))
    user = user_res.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Користувача з таким email не знайдено")

    statement = select(PromoCodeUsage).where(
        PromoCodeUsage.user_id == user.id,
        PromoCodeUsage.promo_id == promo_code.id
    )

    result: Result = await session.execute(statement)
    existing = result.scalar_one_or_none()

    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ви вже використовували цей купон")

    usage = PromoCodeUsage(
        user_id=user.id,
        promo_id=promo_code.id,
        used_at=datetime.utcnow()
    )

    session.add(usage)

    await increment_promo_code_usage(session, promo_code)

    await session.commit()
    await session.refresh(usage)
    return usage


async def get_all_promo_usages(session: AsyncSession, user_email: str):
    user_select = await session.execute(select(User).where(User.email == user_email))
    user = user_select.scalar_one_or_none()

    statement = select(PromoCodeUsage).where(PromoCodeUsage.user_id == user.id)
    result = await session.execute(statement)
    return result.scalars().all()


async def get_usages_by_promo(session: AsyncSession, promo_id: int):
    statement = select(PromoCodeUsage).where(PromoCodeUsage.promo_id == promo_id)
    result = await session.execute(statement)
    return result.scalars().all()