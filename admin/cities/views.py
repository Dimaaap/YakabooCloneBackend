from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from core.models import db_helper
from .forms import CityEditForm
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


@router.get("/{city_id}", response_class=HTMLResponse)
async def get_city_by_id(request: Request, city_id: int,
                         session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    city = await crud.get_city_field_data(session, city_id)
    data = city.model_dump()

    return templates.TemplateResponse(
        "pages/detail.html",
        context={
            "request": request,
            "data": data,
            "page_title": "Cities",
            "model_name": "City",
        }
    )


@router.get("/{city_id}/edit", response_class=HTMLResponse)
async def edit_city_by_id(request: Request, city_id: int,
                          session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    city = await crud.get_city_field_data(session, city_id)

    identifier = city.title
    form = CityEditForm(data=city.model_dump())

    return templates.TemplateResponse(
        "pages/edit.html",
        {
            "request": request,
            "form": form,
            "page_title": "Edit Cities",
            "model_name": "City",
            "identifier": identifier
        }
    )


@router.post("/{author_id}/edit", response_class=HTMLResponse)
async def edit_city_submit(request: Request, city_id: int,
                           session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    form_data = await request.form()
    form = CityEditForm(data=form_data)

    print(form_data)

    return templates.TemplateResponse(
        "pages/edit.html",
        {
            "request": request,
            "form": form,
            "page_title": "Edit Cities",
            "model_name": "City",
            "identifier": city_id
        }
    )