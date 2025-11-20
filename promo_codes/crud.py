from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from promo_codes.schema import PromoCodeCreate, PromoCodeSchema, PromoCodeUpdate, PromoCodeUpdatePartial
from core.models import PromoCode


async def create_promo_code(session: AsyncSession, promo_code: PromoCodeCreate) -> PromoCode:
    new_promo_code = PromoCode(**promo_code.model_dump())

    try:
        session.add(new_promo_code)
        await session.commit()

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return new_promo_code


async def get_all_promo_codes(session: AsyncSession) -> list[PromoCodeSchema]:
    statement = select(PromoCode).where(PromoCode.active).order_by(PromoCode.id)
    result: Result = await session.execute(statement)
    promo_codes = result.scalars().all()
    return promo_codes


async def get_promo_code_by_id(session: AsyncSession, promo_id: int) -> PromoCode:
    statement = select(PromoCode).where(PromoCode.id == promo_id, PromoCode.active)
    result: Result = await session.execute(statement)
    promo_code = result.scalars().first()
    return promo_code


async def get_promo_code_by_code(session: AsyncSession, code: str) -> PromoCode:
    statement = select(PromoCode).where(PromoCode.code == code, PromoCode.active)
    result: Result = await session.execute(statement)
    promo_code = result.scalars().first()
    return promo_code


async def update_promo_code(session: AsyncSession, promo_code_id: int, data: PromoCodeUpdate):
    promo_code = await get_promo_code_by_id(session, promo_code_id)

    if not promo_code:
        raise HTTPException(status_code=404, detail="Promo Code not found")

    for key, value in data.model_dump().items():
        setattr(promo_code, key, value)

    await session.commit()
    await session.refresh(promo_code)
    return promo_code


async def update_promo_code_partial(session: AsyncSession, promo_code_id: int, data: PromoCodeUpdatePartial):
    promo_code = await get_promo_code_by_id(session, promo_code_id)

    if not promo_code:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promo Code not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(promo_code, key, value)

    await session.commit()
    await session.refresh(promo_code)
    return promo_code


async def delete_promo_code_by_id(session: AsyncSession, promo_code_id: int):
    promo_code = await get_promo_code_by_id(session, promo_code_id)

    if not promo_code:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promo Code not found")

    await session.delete(promo_code)
    await session.commit()
    return True


async def validate_promo_code_for_use(session: AsyncSession, code: str):
    promo_code = await get_promo_code_by_code(session, code)

    if not promo_code:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'Код купону "{code}" не дійсний або його неможливо застосувати на це замовлення')

    if not promo_code.active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Купон не активний")

    if promo_code.expires_at and promo_code.expires_at.replace(tzinfo=None) < datetime.utcnow():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Купон {code} прострочений')

    if promo_code.current_uses >= promo_code.max_uses:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Ліміт використання купону вичерпано')

    return promo_code


async def increment_promo_code_usage(session: AsyncSession, promo_code: PromoCode):
    promo_code.current_uses += 1

    if promo_code.current_uses >= promo_code.max_uses:
        promo_code.active = False

    await session.commit()
    await session.refresh(promo_code)
    return promo_code
