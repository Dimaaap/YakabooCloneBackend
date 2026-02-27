from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from core.models import db_helper
from .schema import CitiesListForAdmin
from ..config import templates
from . import crud

router = APIRouter()


@router.get("/list", response_class=HTMLResponse)
async def cities_list(request: Request, session: AsyncSession = Depends(db_helper.scoped_session_dependency)):

    cities = await crud.get_cities_list_for_admin_page(session)
    cities = [city.model_dump() for city in cities]
    fields = list(CitiesListForAdmin.model_fields.keys())
    link_fields = ["country_title"]

    return templates.TemplateResponse(
        "pages/list.html",
        context={
            "request": request,
            "data": cities,
            "page_title": "All Cities",
            "model_name": "City",
            "fields": fields,
            "is_editable": True,
            "is_deletable": True,
            "can_create": True,
            "link_fields": link_fields,
        }
    )