import json

from fastapi import APIRouter, Depends, Query
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from entities.search.schema import SearchResponse
from config import redis_client
from core.models import db_helper
from . import crud
from .client import normalize_search_term
from .config import SEARCH_CACHE_EXPIRATION_SECONDS

router = APIRouter(tags=["Global Search"])


@router.get('/', response_model=SearchResponse)
async def global_search_no_user(
        q: str = Query(..., min_length=2),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await global_search_with_user(None, q, session)


@router.get("/", response_model=SearchResponse)
async def global_search_with_user(
        user_email,
        q: str = Query(..., min_length=2),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    normalized_term = normalize_search_term(q)
    key = f"search:{normalized_term}"
    cached_term = await redis_client.get(key)

    if cached_term:
        return json.loads(cached_term)

    response = await crud.search_response(q, session, user_email)
    data = jsonable_encoder(response)

    await redis_client.set(key, json.dumps(data), ex=SEARCH_CACHE_EXPIRATION_SECONDS)
    return response
