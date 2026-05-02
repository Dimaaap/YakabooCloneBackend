from fastapi import HTTPException, status
from sqlalchemy import select, Result, delete
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import AdditionalText
from entities.additional_text.schema import AdditionalTextSchema, AdditionalTextCreate, AdditionalTextUpdate


async def create_additional_text(session: AsyncSession, additional_text: AdditionalTextCreate) -> AdditionalText:
    new_additional_text = AdditionalText(**additional_text.model_dump())

    try:
        session.add(new_additional_text)
        await session.commit()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return additional_text


async def delete_active_additional_text(session: AsyncSession) -> bool:
    statement = delete(AdditionalText).where(AdditionalText.active)

    try:
        await session.execute(statement)
        await session.commit()
        return True
    except Exception as e:
        await session.rollback()
        return False


async def get_current_active_additional_text(session: AsyncSession) -> AdditionalTextSchema | None:
    statement = select(AdditionalText).where(AdditionalText.active)
    result: Result = await session.execute(statement)
    additional_text = result.scalar_one_or_none()
    if additional_text:
        return AdditionalTextSchema.model_validate(additional_text)
    return None


async def update_additional_text(session: AsyncSession, data: AdditionalTextUpdate) -> AdditionalTextSchema:
    additional_text = select(AdditionalText).where(AdditionalText.active)

    if not additional_text:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Text not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(additional_text, key, value)

    try:
        await session.commit()
        await session.refresh(additional_text)
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)
    return AdditionalTextSchema.model_validate(additional_text)


