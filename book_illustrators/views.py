import json

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from publishing.schemas import BookFilters
from .schemas import BookIllustratorSchema, BookIllustratorCreate
from core.models import db_helper
from . import crud
from config import redis_client

router = APIRouter(tags=["Book Illustrators"])
REDIS_KEY = "illustrators"


@router.get("/all", response_model=list[BookIllustratorSchema])
async def get_all_illustrators(session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    cached_illustrators = await redis_client.get(REDIS_KEY)

    if cached_illustrators:
        return json.loads(cached_illustrators)

    illustrators = await crud.get_all_illustrators(session)
    await redis_client.set(REDIS_KEY, json.dumps([illustrator.model_dump() for illustrator in illustrators]))
    return illustrators


@router.get("/{slug}", response_model=BookIllustratorSchema)
async def get_illustrator_by_slug(slug: str, session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    cached_illustrators = await redis_client.get(REDIS_KEY)

    if cached_illustrators:
        illustrators_list = json.loads(cached_illustrators)
        for illustrator in illustrators_list:
            if illustrator["slug"] == slug:
                return illustrator

    else:
        illustrators = await crud.get_all_illustrators(session)
        await redis_client.set(REDIS_KEY, json.dumps([illustrator.model_dump() for illustrator in illustrators]))
        return await crud.get_illustrator_by_slug(session, slug)


@router.get("/search/", response_model=list[BookIllustratorSchema])
async def search_illustrators(
        query: str = Query(...),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    cached_illustrators = await redis_client.get(REDIS_KEY)

    if cached_illustrators:
        illustrators_list = json.loads(cached_illustrators)
        res = []
        for illustrator in illustrators_list:
            if (
                query.lower() in illustrator["first_name"].lower()
                or query.lower() in illustrator["last_name"].lower()
                or query.lower() in f"{illustrator['first_name'].lower()} {illustrator['last_name'].lower()}"
            ):
                res.append(illustrator)
        return res
    else:
        illustrators = await crud.get_all_illustrators(session)
        await redis_client.set(REDIS_KEY, json.dumps([illustrator.model_dump() for illustrator in illustrators]))
        return await crud.get_illustrator_by_slug(session, query)


@router.post("/create")
async def create_illustrator(illustrator: BookIllustratorCreate,
                             session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    new_illustrator = await crud.create_illustrator(session, illustrator)
    if new_illustrator:
        await redis_client.delete(REDIS_KEY)
        return new_illustrator
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(new_illustrator))


@router.delete("/{illustrator_id}")
async def delete_illustrator_by_id(illustrator_id: int,
                                   session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    success = await crud.delete_illustrator_by_id(session, illustrator_id)

    if success:
        return {"message": f"Illustrator with id {illustrator_id} has been deleted"}
    else:
        return {"message": "Deleting error"}


@router.get("/illustrator/{illustrator_id}/books")
async def get_all_illustrator_books(illustrator_id: int,
                                    filter: BookFilters = Query(None),
                                    session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    books, total = await crud.get_all_illustrator_books_by_illustrator_id(session, illustrator_id,
                                                                   limit=filter.limit, offset=filter.offset,
                                                                   filter=filter)
    return {
        "count": total,
        "limit": filter.limit,
        "offset": filter.offset,
        "has_more": filter.offset + filter.limit < total,
        "results": books
    }