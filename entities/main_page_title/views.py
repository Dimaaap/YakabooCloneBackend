from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from entities.main_page_title.schema import MainPageTitleSchema, MainPageTitleCreate
from core.models import db_helper
from . import crud

router = APIRouter(tags=["Main Page Title"])


@router.get("/all", response_model=list[MainPageTitleSchema])
async def get_all_main_page_titles(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    titles = await crud.get_all_main_page_titles(session)
    return titles


@router.post("/create")
async def create_main_page_title(page_data: MainPageTitleCreate,
                                 session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    new_title = await crud.create_main_page_title(session, page_data)
    return new_title


@router.get("/active", response_model=MainPageTitleSchema)
async def get_active_main_page_title(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    title = await crud.get_active_main_page_title(session)
    return title


@router.delete("/{title_id}")
async def delete_page_title(title_id: int,
                            session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    success = await crud.delete_main_page_title_by_id(session, title_id)

    if success:
        return {"message": f"The page title with id {title_id} was deleted"}
    return {"message": "Deleting Failed"}