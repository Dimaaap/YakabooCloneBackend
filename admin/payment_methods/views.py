from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from core.models import db_helper
from .schema import PaymentMethodsForAdmin
from ..config import templates
from . import crud

router = APIRouter(tags=["Payment Methods For Admin"])


@router.get("/list", response_class=HTMLResponse)
async def get_payment_methods(request: Request, session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    payment_methods = await crud.get_payment_methods_for_admin_page(session)
    payment_methods = [method.model_dump() for method in payment_methods]

    fields = list(PaymentMethodsForAdmin.model_fields.keys())
    link_fields = ["country_title", "city_title"]

    return templates.TemplateResponse(
        "pages/list.html",
        context={
            "request": request,
            "data": payment_methods,
            "page_title": "Payment Methods",
            "model_name": "Payment Method",
            "fields": fields,
            "is_editable": True,
            "is_deletable": True,
            "can_create": True,
            "link_fields": link_fields,
        }
    )