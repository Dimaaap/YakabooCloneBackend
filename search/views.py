from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from search.schema import SearchResponse
from core.models import db_helper
from . import crud

router = APIRouter(tags=["Global Search"])

@router.get("/{user_email}", response_model=SearchResponse)
async def global_search(
        user_email,
        q: str = Query(..., min_length=2),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    response = await crud.search_response(q, user_email, session)
    return response