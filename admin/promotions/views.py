from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from core.models import db_helper
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
        "pages/promotions/list.html",
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