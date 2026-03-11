from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse

from core.models import db_helper
from .forms import DoubleSubCategoryEditForm
from .schema import DoubleSubcategoriesForAdminList, EditDoubleSubCategory
from ..config import templates
from . import crud

router = APIRouter(tags=["Admin Double Subcategories"])


@router.get("/list", response_class=HTMLResponse)
async def double_subcategories_list(request: Request, session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    double_subcategories = await crud.get_double_subcategories_for_admin_page(session)
    double_subcategories = [subcategory.model_dump() for subcategory in double_subcategories]

    fields = list(DoubleSubcategoriesForAdminList.model_fields.keys())
    link_fields = ["subcategory_title"]

    return templates.TemplateResponse(
        "pages/list.html",
        context={
            "request": request,
            "data": double_subcategories,
            "page_title": "All Double Subcategories",
            "model_name": "Double Subcategory",
            "fields": fields,
            "is_editable": True,
            "is_deletable": True,
            "can_create": True,
            "link_fields": link_fields,
        }
    )


@router.get("/{double_subcategory_id}", response_class=HTMLResponse)
async def get_double_subcategory_by_id(request: Request, double_subcategory_id: int,
                                       session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    double_subcategory = await crud.get_double_subcategory_field_data(session, double_subcategory_id)
    data = double_subcategory.model_dump()

    return templates.TemplateResponse(
        "pages/detail.html",
        context={
            "request": request,
            "data": data,
            "page_title": "Book Double Subcategories",
            "model_name": "Double Subcategory",
        }
    )


@router.get("/{double_subcategory_id}/edit", response_class=HTMLResponse)
async def edit_double_subcategory_by_id(request: Request, double_subcategory_id: int,
                             session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    double_subcategory = await crud.get_double_subcategory_field_data(session, double_subcategory_id)
    identifier = double_subcategory.title

    form = DoubleSubCategoryEditForm(data=double_subcategory.model_dump())

    return templates.TemplateResponse(
        "pages/edit.html",
        {
            "request": request,
            "form": form,
            "page_title": "Edit Book Double Subcategory",
            "model_name": "Double Subcategory",
            "identifier": identifier
        }
    )

@router.post("/{double_subcategory_id}/edit", name="admin_edit_double_subcategory", response_class=HTMLResponse)
async def edit_double_subcategory_submit(request: Request, double_subcategory_id: int,
                                         session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    form_data = await request.form()
    form = DoubleSubCategoryEditForm(data=form_data)

    double_subcategory = await crud.get_double_subcategory_field_data(session, double_subcategory_id)
    identifier = double_subcategory.title

    if form.validate():
        double_subcategory_data = EditDoubleSubCategory(**form.data)
        await crud.update_double_subcategory(session, double_subcategory_id, double_subcategory_data)

        return RedirectResponse(
            url=request.url_for("admin_edit_double_subcategory", double_subcategory_id=double_subcategory_id),
            status_code=status.HTTP_303_SEE_OTHER
        )

    return templates.TemplateResponse(
        "pages/edit.html",
        {
            "request": request,
            "form": form,
            "page_title": "Edit Book Double Subcategory",
            "model_name": "Double Subcategory",
            "identifier": identifier
        }
    )