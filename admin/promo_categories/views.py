from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse

from core.models import db_helper
from .forms import PromoCategoryEditForm
from .schema import PromoCategoriesForAdmin, EditPromoCategory
from ..config import templates
from . import crud

router = APIRouter(tags=["Promo Categories For Admin Page"])


@router.get("/list", response_class=HTMLResponse)
async def get_promo_categories(request: Request, session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    promo_categories = await crud.get_promo_categories_for_admin_page(session)
    promo_categories = [category.model_dump() for category in promo_categories]

    fields = list(PromoCategoriesForAdmin.model_fields.keys())

    return templates.TemplateResponse(
        "pages/list.html",
        context={
            "request": request,
            "data": promo_categories,
            "fields": fields,
            "page_title": "Promotion Categories",
            "model_name": "Promo Category",
            "is_editable": True,
            "is_deletable": True,
            "can_create": True
        }
    )


@router.get("/{category_slug}", response_class=HTMLResponse)
async def get_promo_category_by_id(request: Request, category_slug: str,
                                   session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    promo_category = await crud.get_promo_categories_field_data(session, category_slug)
    data = promo_category.model_dump()

    return templates.TemplateResponse(
        "pages/detail.html",
        context={
            "request": request,
            "data": data,
            "page_title": "Promotion Categories",
            "model_name": "Promotion Category"
        }
    )


@router.get("/{category_slug}/edit", response_class=HTMLResponse)
async def edit_promo_category_by_id(request: Request, category_slug: str,
                            session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    promo_category = await crud.get_promo_categories_field_data(session, category_slug)

    identifier = promo_category.title

    form = PromoCategoryEditForm(data=promo_category.model_dump())

    return templates.TemplateResponse(
        "pages/edit.html",
        context={
            "request": request,
            "form": form,
            "page_title": "Edit Promo Category",
            "model_name": "Promo Category",
            "identifier": identifier
        }
    )


@router.post("/{category_slug}/edit", name="admin_edit_promo_category", response_class=HTMLResponse)
async def edit_promo_category_submit(request: Request, category_slug: str,
                                session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    form_data = await request.form()
    form = PromoCategoryEditForm(data=form_data)

    promo_category = await crud.get_promo_categories_field_data(session, category_slug)
    identifier = promo_category.title

    if form.validate():
        category_data = EditPromoCategory(**form.data)
        await crud.update_promo_category(session, category_slug, category_data)

        return RedirectResponse(
            url=request.url_for("admin_edit_promo_category", category_slug=category_slug),
            status_code=status.HTTP_303_SEE_OTHER
        )

    return templates.TemplateResponse(
        "pages/edit.html",
        {
            "request": request,
            "form": form,
            "page_title": "Edit Promo Category",
            "model_name": "Promo Category",
            "identifier": identifier
        }
    )
