from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse

from core.models import db_helper
from .forms import BookCategoryEditForm, BookCategoryCreateForm
from .schema import CategoryForAdminList, EditCategory, CreateCategory
from ..config import templates
from . import crud
from ..subcategories.crud import get_subcategories_for_admin_page

router = APIRouter(tags=["Books Categories for Admin Page"])


@router.get("/list", name="admin_categories_list", response_class=HTMLResponse)
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


@router.get("/create", response_class=HTMLResponse)
async def create_category_page(request: Request,
                               session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    form = BookCategoryCreateForm()

    subcategories = await get_subcategories_for_admin_page(session)
    choices = [(sub.id, sub.title) for sub in subcategories]
    form.subcategories_ids.choices = choices

    return templates.TemplateResponse(
        "pages/create.html",
        {
            "request": request,
            "form": form,
            "page_title": "Create New Category",
            "model_name": "Category"
        }
    )


@router.post("/create", name="admin_create_category", response_class=HTMLResponse)
async def create_category_submit(request: Request, session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    form_data = await request.form()
    form = BookCategoryCreateForm(form_data)

    subcategories = await get_subcategories_for_admin_page(session)
    choices = [(sub.id, sub.title) for sub in subcategories]
    form.subcategories_ids.choices = choices

    if form.validate():
        data = form.data

        data["banner_images"] = data["banner_images"].split() if data.get("banner_images") else []
        data["subcategories_ids"] = [int(s) for s in form_data.getlist("subcategories_ids")]

        category_data = CreateCategory(**data)
        await crud.create_book_category(session, category_data)

        return RedirectResponse(
            url=request.url_for("admin_categories_list"),
            status_code=status.HTTP_303_SEE_OTHER
        )

    return templates.TemplateResponse(
        "pages/create.html",
        {
            "request": request,
            "form": form,
            "page_title": "Create New Category",
            "model_name": "Category"
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