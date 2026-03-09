from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from core.models import db_helper
from .forms import PromoCategoryEditForm
from .schema import PromoCategoriesForAdmin
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