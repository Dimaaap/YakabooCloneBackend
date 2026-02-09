import json

from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import LiteraturePeriodSchema, LiteraturePeriodCreate, LiteraturePeriodWithCountSchema
from core.models import db_helper
from . import crud
from config import redis_client

router = APIRouter(tags=["Literature Periods"])
REDIS_KEY = "literature_periods"


@router.get("/all", response_model=list[LiteraturePeriodSchema])
async def get_all_literature_periods(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    cached_periods = await redis_client.get(REDIS_KEY)

    if cached_periods:
        return json.loads(cached_periods)

    periods = await crud.get_all_literature_periods(session)
    await redis_client.set(REDIS_KEY, json.dumps([period.model_dump() for period in periods], default=str))
    return periods


@router.get("/{slug}", response_model=LiteraturePeriodSchema)
async def get_literature_period_by_slug(slug: str,
                                        session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    periods = await crud.get_literature_period_by_slug(session, slug)
    return periods

@router.get("/search/", response_model=list[LiteraturePeriodSchema])
async def search_literature_periods(
        query: str = Query(...),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    cached_periods = await redis_client.get(REDIS_KEY)

    if cached_periods:
        periods_list = json.loads(cached_periods)
        res = []
        for period in periods_list:
            if(
                query.lower() in period["title"].lower()
            ):
                res.append(period)
        return res
    else:
        periods = await crud.get_all_literature_periods(session)
        await redis_client.set(REDIS_KEY, json.dumps([period.model_dump() for period in periods], default=str))
        return await crud.get_literature_periods_by_query(query, session)


@router.post("/create")
async def create_literature_period(period: LiteraturePeriodCreate,
                                   session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    new_period = await crud.create_literature_period(session, period)

    if new_period:
        await redis_client.delete(REDIS_KEY)
        return new_period
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(new_period))


@router.delete("/{period_id}")
async def delete_literature_period_by_id(period_id: int,
                                         session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    success = await crud.delete_literature_period_by_id(session, period_id)
    if success:
        return {"message": f"Literature period with id {period_id} has been deleted"}
    else:
        return {"message": "Deleting error"}


@router.get("/books-count", response_model=list[LiteraturePeriodWithCountSchema])
async def get_literature_periods_with_books_count(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    print("here")
    res = await crud.get_books_count_by_literature_period(session)
    return res


@router.get("/period/{period_id}/books")
async def get_all_books_by_literature_period(period_id: int,
                                             session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    books = await crud.get_all_period_books_by_period_id(session, period_id)
    return books
