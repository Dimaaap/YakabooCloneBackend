import json
from http.client import HTTPResponse

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from entities.additional_text.schema import AdditionalTextSchema, AdditionalTextCreate
from core.models import db_helper
from config import redis_client
from . import crud
from ..banners.views import SIX_DAYS

router = APIRouter(tags=["Additional Text"])
redis_key = "addition_text:current"


@router.get("/active", response_model=AdditionalTextSchema)
async def get_current_active_text(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    cached_text = await redis_client.get(redis_key)

    if cached_text:
        return json.loads(cached_text)

    additional_text = await crud.get_current_active_additional_text(session)
    if additional_text:
        await redis_client.set(redis_key, json.dumps(additional_text.model_dump(mode="json")), ex=SIX_DAYS)
        return additional_text
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no active additional text"
        )


@router.post("/create")
async def create_additional_text(text_data: AdditionalTextCreate,
                                 session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    new_additional_text = await crud.create_additional_text(session, text_data)
    if new_additional_text:
        await redis_client.delete(redis_key)
    return new_additional_text


@router.delete("/active")
async def delete_current_active_text(session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    success = await crud.delete_active_additional_text(session)

    if success:
        await redis_client.delete(redis_key)
        return {"message": "Current active text has been deleted"}
    return {"message": "Error while deleting current active text"}



