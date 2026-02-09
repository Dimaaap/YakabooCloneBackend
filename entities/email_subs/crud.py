from fastapi import HTTPException, status
from sqlalchemy import select, Result
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import EmailSubs
from entities.email_subs.schemas import EmailSubSchema


async def create_email_sub(session: AsyncSession, email: str) -> EmailSubs:
    sub = EmailSubs(email=email)
    try:
        session.add(sub)
        await session.commit()
    except IntegrityError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return sub


async def get_all_subs(session: AsyncSession) -> list[EmailSubSchema]:
    statement = select(EmailSubs).order_by(EmailSubs.id)
    result: Result = await session.execute(statement)
    subs = result.scalars().all()
    return list(subs)


async def check_email_in_subs(session: AsyncSession, email: str):
    try:
        statement = select(1).where(EmailSubs.email == email)
        result = await session.execute(statement)
        exists = result.scalar() is not None
        return {"exists": exists}
    except Exception:
        return {"exists": False}


async def get_sub_by_email(session: AsyncSession, email: str) -> EmailSubSchema | bool:
    statement = select(EmailSubs).where(EmailSubs.email == email)
    result: Result = await session.execute(statement)
    try:
        sub = result.scalars().first()
    except Exception as e:
        return False
    return sub


async def delete_sub_by_email(session: AsyncSession, email: str) -> bool:
    try:
        statement = select(EmailSubs).where(EmailSubs.email == email)
        result = await session.execute(statement)
        sub = result.scalars().first()

        if not sub:
            return True
        await session.delete(sub)
        await session.commit()
        return True
    except SQLAlchemyError as e:
        await session.rollback()
        return False