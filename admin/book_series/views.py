from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from core.models import db_helper
from .forms import BookSeriaEditForm
from .schema import BookSeriesForAdminList
from ..config import templates
from . import crud

router = APIRouter(tags=["Book Series for Admin Page"])


@router.get("/list", response_class=HTMLResponse)
async def series_list(request: Request, session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    series = await crud.get_book_series_for_admin_page(session)
    series = [seria.model_dump() for seria in series]

    fields = list(BookSeriesForAdminList.model_fields.keys())

    return templates.TemplateResponse(
        "pages/list.html",
        context={
            "request": request,
            "data": series,
            "page_title": "All Book Series",
            "model_name": "Book Seria",
            "fields": fields,
            "is_editable": True,
            "is_deletable": True,
            "can_create": True,
        }
    )


@router.get("/{seria_id}", response_class=HTMLResponse)
async def get_book_seria_by_id(request: Request, seria_id: int,
                               session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    book_seria = await crud.get_book_seria_field_data(session, seria_id)
    data = book_seria.model_dump()

    return templates.TemplateResponse(
        "pages/detail.html",
        context={
            "request": request,
            "data": data,
            "page_title": "Book Series",
            "model_name": "Book Seria",
        }
    )


@router.get("/{seria_id}/edit", response_class=HTMLResponse)
async def edit_book_seria_by_id(request: Request, seria_id: int,
                                session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    book_seria = await crud.get_book_seria_field_data(session, seria_id)

    identifier = book_seria.title
    form = BookSeriaEditForm(data=book_seria.model_dump())

    return templates.TemplateResponse(
        "pages/edit.html",
        {
            "request": request,
            "form": form,
            "page_title": "Edit Book Seria",
            "model_name": "Book Seria",
            "identifier": identifier,
        }
    )


@router.post("/{seria_id}/edit", response_class=HTMLResponse)
async def edit_book_seria_submit(request: Request, seria_id: int,
                                 session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    form_data = await request.form()
    form = BookSeriaEditForm(data=form_data)

    print(form_data)

    return templates.TemplateResponse(
        "pages/edit.html",
        {
            "request": request,
            "form": form,
            "page_title": "Edit Book Seria",
            "model_name": "Book Seria",
            "identifier": seria_id
        }
    )