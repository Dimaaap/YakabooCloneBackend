from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from core.models import db_helper
from .forms import PromotionsEditForm
from .schema import PromotionsForAdminPage
from ..config import templates
from . import crud
from ..utils import convert_alchemy_datetime

router = APIRouter(tags=["Promotions For Admin Page"])


@router.get("/list", response_class=HTMLResponse)
async def get_promotions(request: Request, session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    promotions = await crud.get_promotions_for_admin_page(session)
    promotions = [promotion.model_dump() for promotion in promotions]

    for promotion in promotions:
        promotion["end_date"] = convert_alchemy_datetime(promotion["end_date"]) if promotion["end_date"] else None

    fields = list(PromotionsForAdminPage.model_fields.keys())
    link_fields = ["categories_title"]

    return templates.TemplateResponse(
        "pages/list.html",
        context={
            "request": request,
            "data": promotions,
            "fields": fields,
            "page_title": "Promotions",
            "model_name": "Promotion",
            "is_editable": True,
            "is_deletable": True,
            "can_create": True,
            "link_fields": link_fields
        }
    )


@router.get("/{promotion_id}", response_class=HTMLResponse)
async def get_promotion_by_id(request: Request, promotion_id: int,
                              session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    promotion = await crud.get_promotion_field_data(session, promotion_id)
    data = promotion.model_dump()

    return templates.TemplateResponse(
        "pages/detail.html",
        context={
            "request": request,
            "data": data,
            "page_title": "Promotions",
            "model_name": "Promotion"
        }
    )


@router.get("/{promo_id}/edit", response_class=HTMLResponse)
async def edit_promotion_by_id(request: Request, promo_id: int,
                            session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    promo = await crud.get_promotion_field_data(session, promo_id)
    promo_categories = await crud.get_all_categories(session)

    identifier = promo.title

    form = PromotionsEditForm(data=promo.model_dump())

    form.categories_title.choices = [
        (category.title, category.title) for category in promo_categories
    ]

    return templates.TemplateResponse(
        "pages/edit.html",
        context={
            "request": request,
            "form": form,
            "page_title": "Edit Promotion",
            "model_name": "Promotion",
            "identifier": identifier
        }
    )