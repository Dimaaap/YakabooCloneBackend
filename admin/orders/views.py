from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from core.models import db_helper
from .schema import OrdersForAdmin
from ..config import templates
from . import crud
from ..utils import convert_alchemy_datetime

router = APIRouter(tags=["Orders for Admin Page"])


@router.get("/list", response_class=HTMLResponse)
async def get_orders(request: Request, session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    orders = await crud.get_orders_for_admin_page(session)
    orders = [order.model_dump() for order in orders]

    for order in orders:
        order["create_date"] = convert_alchemy_datetime(order["create_date"])

    fields = list(OrdersForAdmin.model_fields.keys())
    link_fields = ["user_email", "city_title", "country_title",
                   "new_post_number", "new_post_postomat",
                   "ukrpost_office", "meest_post_office",
                   "promo_usage"]
    return templates.TemplateResponse(
        "pages/list.html",
        context={
            "request": request,
            "data": orders,
            "page_title": "Orders",
            "model_name": "Order",
            "fields": fields,
            "is_editable": True,
            "is_deletable": True,
            "can_create": True,
            "link_fields": link_fields,
        }
    )
