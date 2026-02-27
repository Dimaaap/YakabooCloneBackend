from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from core.models import db_helper
from .schema import PromoCodesAdminList
from ..config import templates
from . import crud
from ..utils import convert_alchemy_datetime

router = APIRouter(tags=["Promo Codes For Admin Page"])


@router.get("/list", response_class=HTMLResponse)
async def get_promo_codes(request: Request, session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    promo_codes = await crud.get_promo_codes_for_admin_page(session)
    promo_codes = [code.model_dump() for code in promo_codes]

    for code in promo_codes:
        code["expires_at"] = convert_alchemy_datetime(code["expires_at"])

    fields = list(PromoCodesAdminList.model_fields.keys())

    return templates.TemplateResponse(
        "pages/list.html",
        context={
            "request": request,
            "data": promo_codes,
            "fields": fields,
            "page_title": "Promo Codes",
            "model_name": "Promo Code",
            "is_editable": True,
            "is_deletable": True,
            "can_create": True,
        }
    )