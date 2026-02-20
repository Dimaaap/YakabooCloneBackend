from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from core.models import db_helper
from .schema import DeliveryTermsForAdminList
from ..config import templates
from . import crud

router = APIRouter(tags=["Admin Delivery Terms"])


@router.get("/list", response_class=HTMLResponse)
async def delivery_terms_list(request: Request, session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    delivery_terms = await crud.get_delivery_terms_list_for_admin_page(session)
    delivery_terms = [term.model_dump() for term in delivery_terms]

    fields = list(DeliveryTermsForAdminList.model_fields.keys())
    link_fields = ["country_title", "city_title"]

    return templates.TemplateResponse(
        "pages/delivery_terms/list.html",
        context={
            "request": request,
            "data": delivery_terms,
            "page title": "All Delivery Terms",
            "model_name": "Delivery Term",
            "fields": fields,
            "is_editable": True,
            "is_deletable": True,
            "link_fields": link_fields,
        }
    )