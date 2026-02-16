from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from core.models import db_helper
from .schema import CountriesListForAdmin
from ..config import templates
from . import crud

router = APIRouter(tags=["Admin Countries"])


@router.get("/list", response_class=HTMLResponse)
async def countries_list(request: Request, session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    countries = await crud.get_countries_list_for_admin_page(session)
    countries = [country.model_dump() for country in countries]

    fields = list(CountriesListForAdmin.model_fields.keys())

    return templates.TemplateResponse(
        "pages/countries/list.html",
        context={
            "request": request,
            "data": countries,
            "page_title": "All Countries",
            "model_name": "Country",
            "fields": fields,
            "is_editable": True,
            "is_deletable": True,
            "can_create": True
        }
    )