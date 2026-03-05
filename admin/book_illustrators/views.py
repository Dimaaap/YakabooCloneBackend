from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from core.models import db_helper
from .forms import BookIllustratorEditForm
from .schema import BookIllustratorsListForAdmin
from ..config import templates
from . import crud


router = APIRouter(tags=["Book Illustrators for Admin Page"])


@router.get("/list", response_class=HTMLResponse)
async def book_illustrators_list(request: Request,
                                 session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    illustrators = await crud.get_book_illustrator_for_admin_page(session)
    illustrators = [illustrator.model_dump() for illustrator in illustrators]
    fields = list(BookIllustratorsListForAdmin.model_fields.keys())

    return templates.TemplateResponse(
        "pages/list.html",
        context={
            "request": request,
            "data": illustrators,
            "page_title": "All Book Illustrators",
            "model_name": "Book Illustrator",
            "fields": fields,
            "is_editable": True,
            "is_deletable": True,
            "can_create": True
        }
    )

@router.get("/{illustrator_id}", response_class=HTMLResponse)
async def get_book_illustrator_by_id(request: Request, illustrator_id: int,
                                     session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    book_illustrator = await crud.get_book_illustrator_field_data(session, illustrator_id)
    data = book_illustrator.model_dump()

    return templates.TemplateResponse(
        "pages/detail.html",
        context={
            "request": request,
            "data": data,
            "page_title": "Book Illustrators",
            "model_name": "Book Illustrator",
        }
    )


@router.get("/{illustrator_id}/edit", response_class=HTMLResponse)
async def edit_book_illustrator_by_id(request: Request, illustrator_id: int,
                                      session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    illustrator = await crud.get_book_illustrator_field_data(session, illustrator_id)

    identifier = f"{illustrator.first_name} {illustrator.last_name}"
    form = BookIllustratorEditForm(data=illustrator.model_dump())

    return templates.TemplateResponse(
        "pages/edit.html",
        context={
            "request": request,
            "form": form,
            "page_title": "Edit Book Illustrator",
            "model_name": "Book Illustrator",
            "identifier": identifier
        }
    )


@router.post("/{illustrator_id}/edit", response_class=HTMLResponse)
async def edit_book_illustrator_submit(request: Request, illustrator_id: int,
                                       session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    form_data = await request.form()
    form = BookIllustratorEditForm(data=form_data)

    print(form_data)

    return templates.TemplateResponse(
        "pages/edit.html",
        {
            "request": request,
            "form": form,
            "page_title": "Edit Book Illustrator",
            "model_name": "Book Illustrator",
            "identifier": illustrator_id
        }
    )