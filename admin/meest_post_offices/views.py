from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from core.models import db_helper
from .schema import MeestPostOfficesForAdmin
from ..config import templates
from . import crud

router = APIRouter(tags=["Meest Post Offices for Admin Page"])


@router.get("/list", response_class=HTMLResponse)
async def get_meest_post_offices(request: Request, session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    meest_offices = await crud.get_meest_post_offices_for_admin_page(session)
    meest_offices = [office.model_dump() for office in meest_offices]

    fields = list(MeestPostOfficesForAdmin.model_fields.keys())
    link_fields = ["city_title"]

    return templates.TemplateResponse(
        "pages/list.html",
        context={
            "request": request,
            "data": meest_offices,
            "page_title": "Meest Post Offices",
            "model_name": "Meest Post Office",
            "fields": fields,
            "is_editable": True,
            "is_deletable": True,
            "can_create": True,
            "link_fields": link_fields,
        }
    )