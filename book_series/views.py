from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from .schema import BookSeriaSchema, BookSeriaCreate
from core.models import db_helper
from . import crud

router = APIRouter(tags=["Book Series"])


@router.get('/all', response_model=list[BookSeriaSchema])
async def get_all_series(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await crud.get_all_series(session)


@router.get('/{slug}', response_model=BookSeriaSchema)
async def get_seria_by_slug(slug: str, session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await crud.get_seria_by_slug(slug, session)


@router.get('/search/', response_model=list[BookSeriaSchema])
async def search_series(
        query: str = Query(...),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.get_series_by_query(query, session)


@router.post('/create')
async def create_seria(seria: BookSeriaCreate, session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    new_seria = await crud.create_seria(session, seria)
    if new_seria:
        return new_seria
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(new_seria))