from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse

from core.models import db_helper
from .forms import BookCategoryEditForm
from .schema import CategoryForAdminList, EditCategory
from ..config import templates
from . import crud

router = APIRouter(tags=["Books Categories for Admin Page"])


@router.get("/list", response_class=HTMLResponse)
async def categories_list(request: Request, session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    categories = await crud.get_categories_for_admin_page(session)
    categories = [category.model_dump() for category in categories]
    fields = list(CategoryForAdminList.model_fields.keys())
    link_fields = ["subcategories_title", "banner_images"]

    return templates.TemplateResponse(
        "pages/list.html",
        context={
            "request": request,
            "data": categories,
            "page_title": "All Categories",
            "model_name": "Category",
            "fields": fields,
            "is_editable": True,
            "is_deletable": True,
            "can_create": True,
            "link_fields": link_fields
        }
    )


@router.get("/{category_id}", response_class=HTMLResponse)
async def get_category_by_id(request: Request, category_id: int,
                             session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    category = await crud.get_category_field_data(session, category_id)
    data = category.model_dump()

    return templates.TemplateResponse(
        "pages/detail.html",
        context={
            "request": request,
            "data": data,
            "page_title": "Book Categories",
            "model_name": "Book Category",
        }
    )


@router.get("/{category_id}/edit", response_class=HTMLResponse)
async def edit_book_category_by_id(request: Request, category_id: int,
                                   session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    category = await crud.get_category_field_data(session, category_id)

    identifier = category.title
    form = BookCategoryEditForm(data=category.model_dump())

    return templates.TemplateResponse(
        "pages/edit.html",
        {
            "request": request,
            "form": form,
            "page_title": "Edit Book Category",
            "model_name": "Book Category",
            "identifier": identifier
        }
    )


@router.post("/{category_id}/edit", name="admin_edit_category", response_class=HTMLResponse)
async def edit_book_category_submit(request: Request, category_id: int,
                                    session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    form_data = await request.form()
    form = BookCategoryEditForm(data=form_data)

    category = await crud.get_category_field_data(session, category_id)
    identifier = category.title

    if form.validate():
        category_date = EditCategory(**form.data)
        await crud.update_book_category(session, category_id, category_date)

        return RedirectResponse(
            url=request.url_for("admin_edit_category", category_id=category_id),
            status_code=status.HTTP_303_SEE_OTHER
        )

    return templates.TemplateResponse(
        "pages/edit.html",
        {
            "request": request,
            "form": form,
            "page_title": "Edit Book Category",
            "model_name": "Book Category",
            "identifier": identifier
        }
    )