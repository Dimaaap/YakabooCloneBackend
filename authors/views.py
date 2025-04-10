from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import AuthorSchema, AuthorCreate
from core.models import db_helper
from . import crud

router = APIRouter(tags=["authors"])


@router.get("/all", response_model=list[AuthorSchema])
async def get_all_authors(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await crud.get_all_authors(session)


@router.post("/create")
async def create_author(author: AuthorCreate,
                        session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    new_author = await crud.create_author(session, author)
    return new_author


@router.delete("/{author_id}")
async def delete_author_by_id(author_id: int,
                              session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    success = await crud.delete_author_by_id(session, author_id)
    if success:
        return {"message": f"Author with id {author_id} has been deleted"}
    else:
        return {"message": "Deleting error"}
