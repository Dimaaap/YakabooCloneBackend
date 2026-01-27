from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy import select, update, Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User, UserSearchHistory

LAST_HISTORY_TERMS_COUNT = 5


async def add_term_to_search_history(session: AsyncSession, user_email: str, term: str, is_active: bool = True):
    user_res = await session.execute(select(User).where(User.email == user_email))
    user: Result = user_res.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    statement = select(UserSearchHistory).where(UserSearchHistory.term == term)

    result: Result = await session.execute(statement)
    existing = result.scalar_one_or_none()

    if existing:
        return {}

    new_search_term = UserSearchHistory(user_id=user.id, is_active=is_active, term=term, term_date=datetime.utcnow())
    session.add(new_search_term)
    await session.commit()
    await session.refresh(new_search_term)
    return new_search_term


async def get_all_user_search_terms(session: AsyncSession, user_email: str):
    user_select = await session.execute(select(User).where(User.email == user_email))
    user: Result = user_select.scalar_one_or_none()

    statement = (select(UserSearchHistory)
                 .where(UserSearchHistory.user_id == user.id, UserSearchHistory.is_active)
                 .order_by(UserSearchHistory.term_date.desc())
                 .limit(LAST_HISTORY_TERMS_COUNT))

    result: Result = await session.execute(statement)
    return result.unique().scalars().all()


async def clear_all_user_search_terms(session: AsyncSession, user_email: str):
    user_select = await session.execute(select(User).where(User.email == user_email))
    user: Result = user_select.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    statement = update(UserSearchHistory).where(UserSearchHistory.user_id == user.id).values(is_active=False)
    await session.execute(statement)
    await session.commit()

    return {"success": True}

