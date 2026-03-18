from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse

from core.models import db_helper
from .forms import SubCategoryEditForm
from .schema import SubCategoriesForAdminList, EditSubCategory
from ..config import templates
from . import crud

router = APIRouter(tags=["Admin Subcategories"])


@router.get("/list", response_class=HTMLResponse)
async def subcategories_list(request: Request, session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    subcategories = await crud.get_subcategories_for_admin_page(session)
    subcategories = [sub.model_dump() for sub in subcategories]

    fields = list(SubCategoriesForAdminList.model_fields.keys())
    link_fields = ["category_title"]

    return templates.TemplateResponse(
        "pages/list.html",
        context={
            "request": request,
            "data": subcategories,
            "page_title": "All Book Subcategories",
            "model_name": "Subcategory",
            "fields": fields,
            "is_editable": True,
            "is_deletable": True,
            "can_create": True,
            "link_fields": link_fields
        }
    )


@router.get("/{subcategory_id}", response_class=HTMLResponse)
async def get_subcategory_by_id(request: Request, subcategory_id: int,
                                session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    subcategory = await crud.get_subcategory_field_data(session, subcategory_id)
    data = subcategory.model_dump()

    return templates.TemplateResponse(
        "pages/detail.html",
        context={
            "request": request,
            "data": data,
            "page_title": "Book Subcategory",
            "model_name": "Subcategory"
        }
    )


@router.get("/{subcategory_id}/edit", response_class=HTMLResponse)
async def edit_subcategory_by_id(request: Request, subcategory_id: int,
                                 session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    subcategory = await crud.get_subcategory_field_data(session, subcategory_id)
    identifier = subcategory.title

    form = SubCategoryEditForm(data=subcategory.model_dump())

    return templates.TemplateResponse(
        "pages/edit.html",
        {
            "request": request,
            "form": form,
            "page_title": "Edit Book Subcategory",
            "model_name": "Subcategory",
            "identifier": identifier
        }
    )


@router.post("/{subcategory_id}/edit", name="admin_edit_subcategory", response_class=HTMLResponse)
async def edit_subcategory_submit(request: Request, subcategory_id: int,
                                  session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    form_data = await request.form()
    form = SubCategoryEditForm(data=form_data)

    subcategory = await crud.get_subcategory_field_data(session, subcategory_id)
    identifier = subcategory.title

    if form.validate():
        subcategory_data = EditSubCategory(**form.data)
        await crud.update_subcategory(session, subcategory_id, subcategory_data)

        return RedirectResponse(
            url=request.url_for("admin_edit_subcategory"),
            status_code=status.HTTP_303_SEE_OTHER
        )

    return templates.TemplateResponse(
        "pages/edit.html",
        {
            "request": request,
            "form": form,
            "page_title": "Edit Book Subcategory",
            "model_name": "Subcategory",
            "identifier": identifier
        }
    )