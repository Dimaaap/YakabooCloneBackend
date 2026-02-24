from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from core.models import db_helper
from .schema import PromoCodeUsagesForAdmin
from ..config import templates
from . import crud
from ..utils import convert_alchemy_datetime

router = APIRouter(tags=["Promo Code Usages For Admin Page"])


@router.get("/list", response_class=HTMLResponse)
async def get_promo_code_usages(request: Request, session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    promo_code_usages = await crud.get_promo_code_usages_for_admin_page(session)
    promo_code_usages = [usage.model_dump() for usage in promo_code_usages]

    for usage in promo_code_usages:
        usage["used_at"] = convert_alchemy_datetime(usage["used_at"])

    fields = list(PromoCodeUsagesForAdmin.model_fields.keys())
    links_list = ["user_email", "promo_code_title"]

    return templates.TemplateResponse(
        "pages/promo_code_usages/list.html",
        context={
            "request": request,
            "data": promo_code_usages,
            "fields": fields,
            "page_title": "Promo Code Usages",
            "model_name": "Promo Code Usage",
            "is_editable": True,
            "is_deletable": True,
            "can_create": True,
            "link_fields": links_list
        }
    )