from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse

from core.models import db_helper
from .crud import set_subcategories_in_choices
from .forms import DoubleSubCategoryEditForm, DoubleSubCategoryCreateForm
from .schema import DoubleSubcategoriesForAdminList, EditDoubleSubCategory, CreateDoubleSubCategory
from ..config import templates
from . import crud

router = APIRouter(tags=["Admin Double Subcategories"])


@router.get("/list", name="admin_double_subcategories_list", response_class=HTMLResponse)
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


@router.get("/create", response_class=HTMLResponse)
async def create_double_subcategory_page(request: Request,
                                         session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    form = DoubleSubCategoryCreateForm()

    await set_subcategories_in_choices(session, form)

    return templates.TemplateResponse(
        "pages/create.html",
        {
            "request": request,
            "form": form,
            "page_title": "Create Double Subcategory",
            "model_name": "Double Subcategory"
        }
    )


@router.post("/create", name="admin_create_double_subcategory", response_class=HTMLResponse)
async def create_double_subcategory_submit(request: Request,
                                           session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    form_data = await request.form()
    form = DoubleSubCategoryCreateForm(form_data)

    await set_subcategories_in_choices(session, form)

    if form.validate():
        data = dict(form_data)
        data["subcategory_id"] = int(data["subcategory_id"])

        images_raw = data.get("images_src", "")
        data["images_src"] = images_raw.split() if images_raw else []

        double_subcategories_form_data = CreateDoubleSubCategory(**data)

        await crud.create_double_subcategory(session, double_subcategories_form_data)
        return RedirectResponse(url=request.url_for("admin_double_subcategories_list"),
                                status_code=status.HTTP_303_SEE_OTHER)

    return templates.TemplateResponse(
        "pages/create.html",
        {
            "request": request,
            "form": form,
            "page_title": "Create Double Subcategory",
            "model_name": "Double Subcategory"
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