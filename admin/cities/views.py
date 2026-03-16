from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse

from core.models import db_helper
from .forms import CityEditForm, CityCreateForm
from .schema import CitiesListForAdmin, EditCity, CreateCity
from ..config import templates
from . import crud

router = APIRouter()


@router.get("/list", name="admin_cities_list", response_class=HTMLResponse)
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


@router.get("/create", response_class=HTMLResponse)
async def create_country_page(request: Request, session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    form = CityCreateForm()

    await crud.set_countries_in_choices(session, form)

    return templates.TemplateResponse(
        "pages/create.html",
        {
            "request": request,
            "form": form,
            "page_title": "Create City",
            "model_name": "City",
        }
    )


@router.post("/create", name="admin_create_city", response_class=HTMLResponse)
async def create_country_submit(request: Request, session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    form_data = await request.form()
    form = CityCreateForm(form_data)

    await crud.set_countries_in_choices(session, form)

    if form.validate():
        city_data = CreateCity(**form_data)

        city = await crud.create_city(session, city_data)

        return RedirectResponse(url=request.url_for("admin_cities_list"), status_code=status.HTTP_303_SEE_OTHER)

    return templates.TemplateResponse(
        "pages/create.html",
        {
            "request": request,
            "form": form,
            "page_title": "Create City",
            "model_name": "City"
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

    await crud.set_countries_in_choices(session, form)

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


@router.post("/{city_id}/edit", name="admin_edit_city", response_class=HTMLResponse)
async def edit_city_submit(request: Request, city_id: int,
                           session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    form_data = await request.form()
    form = CityEditForm(form_data)

    await crud.set_countries_in_choices(session, form)

    city = await crud.get_city_field_data(session, city_id)
    identifier = city.title

    if form.validate():
        city_data = EditCity(**form_data)
        await crud.update_city(session, city_id, city_data)

        return RedirectResponse(
            url=request.url_for("admin_edit_city", city_id=city_id),
            status_code=status.HTTP_303_SEE_OTHER
        )

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