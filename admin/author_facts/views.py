from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from core.models import db_helper
from .schema import AuthorFactsForAdminPage
from ..config import templates
from . import crud

router = APIRouter(tags=["Author Facts For Admin Page"])


@router.get("/list", response_class=HTMLResponse)
async def author_facts_list(request: Request, session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    author_facts = await crud.get_author_facts_for_admin_page(session)
    author_facts = [fact.model_dump() for fact in author_facts]

    fields = list(AuthorFactsForAdminPage.model_fields.keys())
    link_fields = ["author_name"]

    return templates.TemplateResponse(
        "pages/list.html",
        context={
            "request": request,
            "data": author_facts,
            "page_title": "Author Facts",
            "model_name": "Author Fact",
            "fields": fields,
            "is_editable": True,
            "is_deletable": True,
            "can_create": True,
            "link_fields": link_fields,
        }
    )

@router.get("/{fact_id}", response_class=HTMLResponse)
async def get_author_fact_by_id(request: Request, fact_id: int,
                                session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    author_fact = await crud.get_author_fact_field_data(session, fact_id)
    data = author_fact.model_dump()


    return templates.TemplateResponse(
        "pages/detail.html",
        context={
            "request": request,
            "data": data,
            "page_title": "Author Facts",
            "model_name": "Author Fact"
        }
    )