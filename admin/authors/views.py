from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from core.models import db_helper
from .schema import AuthorsListForAdmin
from ..config import templates
from . import crud

router = APIRouter(tags=["Authors for Admin Page"])


@router.get("/list", response_class=HTMLResponse)
async def authors_list(request: Request, session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    authors = await crud.get_authors_list_for_admin_page(session)
    authors = [author.model_dump() for author in authors]
    fields = list(AuthorsListForAdmin.model_fields.keys())
    link_fields = ["images_src", "interesting_fact"]

    return templates.TemplateResponse(
        "pages/list.html",
        context={
            "request": request,
            "data": authors,
            "page_title": "All Authors",
            "model_name": "Author",
            "fields": fields,
            "is_editable": True,
            "is_deletable": True,
            "can_create": True,
            "link_fields": link_fields,
        }
    )


@router.get("/{author_id}", response_class=HTMLResponse)
async def get_author_by_id(request: Request, author_id: int,
                           session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    author = await crud.get_author_field_data(session, author_id)
    data = author.model_dump()

    return templates.TemplateResponse(
        "pages/detail.html",
        context={
            "request": request,
            "data": data,
            "page_title": "Authors",
            "model_name": "Author",
        }
    )