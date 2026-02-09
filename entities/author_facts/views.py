from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import AuthorFactSchema
from core.models import db_helper
from . import crud

router = APIRouter(tags=["Author Facts"])


@router.get("/all", response_model=list[AuthorFactSchema])
async def get_all_author_facts(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await crud.get_all_author_facts(session)


@router.get('/author/{author_id}')
async def get_fact_by_author_id(author_id: int,
                                session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    author = await crud.get_fact_by_author_id(author_id, session)
    if author:
        return author
    return {}


