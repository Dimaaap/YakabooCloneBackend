from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from core.models import db_helper
from .forms import CountryEditForm
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
        "pages/list.html",
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


@router.get("/{country_id}", response_class=HTMLResponse)
async def get_country_by_id(request: Request, country_id: int,
                            session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    country = await crud.get_country_field_data(session, country_id)
    data = country.model_dump()

    return templates.TemplateResponse(
        "pages/detail.html",
        context={
            "request": request,
            "data": data,
            "page_title": "Countries",
            "model_name": "Country"
        }
    )


@router.get("/{country_id}/edit", response_class=HTMLResponse)
async def get_country_by_id(request: Request, country_id: int,
                            session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    country = await crud.get_country_field_data(session, country_id)

    identifier = country.title

    form = CountryEditForm(data=country.model_dump())

    return templates.TemplateResponse(
        "pages/edit.html",
        context={
            "request": request,
            "form": form,
            "page_title": "Edit Country",
            "model_name": "Country",
            "identifier": identifier
        }
    )


@router.post("/{author_id}/edit", response_class=HTMLResponse)
async def edit_country_submit(request: Request, country_id: int,
                              session: AsyncSession = Depends(db_helper.scoped_session_dependency)):

    form_data = await request.form()
    form = CountryEditForm(form_data)

    print(form_data)

    return templates.TemplateResponse(
        "pages/edit.html",
        {
            "request": request,
            "form": form,
            "page_title": "Edit Country",
            "model_name": "Country",
            "identifier": country_id,
        }
    )