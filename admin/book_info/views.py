from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse

from core.models import db_helper
from .forms import BookInfoEditForm
from .schema import BookInfoListForAdmin, EditBookInfo
from ..config import templates
from . import crud

router = APIRouter(tags=["Book Info List for Admin Page"])


@router.get("/list", response_class=HTMLResponse)
async def book_info_list(request: Request, session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    book_info = await crud.get_book_info_list_for_admin_page(session)
    book_info = [info.model_dump() for info in book_info]

    fields = list(BookInfoListForAdmin.model_fields.keys())
    link_fields = ["book_title"]

    return templates.TemplateResponse(
        "pages/list.html",
        context={
            "request": request,
            "data": book_info,
            "page_title": "All Book Info List",
            "model_name": "Book Info",
            "fields": fields,
            "is_editable": True,
            "is_deletable": True,
            "can_create": True,
            "link_fields": link_fields
        }
    )

@router.get("/{book_info_id}", response_class=HTMLResponse)
async def get_book_info_by_id(request: Request, book_info_id: int,
                              session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    book_info = await crud.get_book_info_field_data(session, book_info_id)
    data = book_info.model_dump()

    return templates.TemplateResponse(
        "pages/detail.html",
        context={
            "request": request,
            "data": data,
            "page_title": "Book Info Details",
            "model_name": "Book Info"
        }
    )


@router.get("/{book_info_id}/edit", response_class=HTMLResponse)
async def edit_book_info_by_id(request: Request, book_info_id: int,
                               session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    book_info = await crud.get_book_info_field_data(session, book_info_id)

    identifier = book_info.book_title

    form = BookInfoEditForm(data=book_info.model_dump())

    return templates.TemplateResponse(
        "pages/edit.html",
        {
            "request": request,
            "form": form,
            "page_title": "Edit Book Info",
            "model_name": "Book Info",
            "identifier": identifier,
        }
    )


@router.post("/{book_info_id}/edit", name="admin_edit_book_info", response_class=HTMLResponse)
async def edit_book_info_submit(request: Request, book_info_id: int,
                                session: AsyncSession = Depends(db_helper.scoped_session_dependency)):

    form_data = await request.form()
    form = BookInfoEditForm(data=form_data)

    book_info = await crud.get_book_info_field_data(session, book_info_id)
    identifier = book_info.book_title

    if form.validate():
        book_info_data = EditBookInfo(**form.data)
        await crud.update_book_info(session, book_info_id, book_info_data)

        return RedirectResponse(
            url=request.url_for("admin_edit_book_info", book_info_id=book_info_id),
            status_code=status.HTTP_303_SEE_OTHER
        )


    return templates.TemplateResponse(
        "pages/edit.html",
        {
            "request": request,
            "form": form,
            "page_title": "Edit Book Info",
            "model_name": "Book Info",
            "identifier": identifier
        }
    )
