from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from core.models import db_helper
from .forms import PublishingEditForm
from .schema import PublishingListForAdmin
from ..config import templates
from . import crud

router = APIRouter(tags=["Publishing List For Admin"])


@router.get("/list", response_class=HTMLResponse)
async def get_publishing_list(request: Request, session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    publishing_list = await crud.get_publishing_list_for_admin_page(session)
    publishing_list = [publishing.model_dump() for publishing in publishing_list]

    fields = list(PublishingListForAdmin.model_fields.keys())

    return templates.TemplateResponse(
        "pages/list.html",
        context={
            "request": request,
            "data": publishing_list,
            "fields": fields,
            "page_title": "Publishing List",
            "model_name": "Publishing",
            "is_editable": True,
            "is_deletable": True,
            "can_create": True,
        }
    )

@router.get("/{publishing_id}", response_class=HTMLResponse)
async def get_publishing_by_id(request: Request, publishing_id: int,
                               session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    publishing = await crud.get_publishing_field_data(session, publishing_id)
    data = publishing.model_dump()

    return templates.TemplateResponse(
        "pages/detail.html",
        context={
            "request": request,
            "data": data,
            "page_title": "Book Publishing List",
            "model_name": "Publishing"
        }
    )


@router.get("/{publishing_id}/edit", response_class=HTMLResponse)
async def edit_publishing_by_id(request: Request, publishing_id: int,
                            session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    publishing = await crud.get_publishing_field_data(session, publishing_id)
    identifier = publishing.title

    form = PublishingEditForm(data=publishing.model_dump())

    return templates.TemplateResponse(
        "pages/edit.html",
        context={
            "request": request,
            "form": form,
            "page_title": "Edit Publishing",
            "model_name": "Publishing",
            "identifier": identifier
        }
    )