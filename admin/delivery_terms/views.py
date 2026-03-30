from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse

from core.models import db_helper
from .crud import set_cities_in_choices
from .forms import DeliveryTermEditForm, DeliveryTermCreateForm
from .schema import DeliveryTermsForAdminList, EditDeliveryTerm, CreateDeliveryTerm
from ..cities.crud import set_countries_in_choices
from ..config import templates
from . import crud

router = APIRouter(tags=["Admin Delivery Terms"])


@router.get("/list", name="admin_delivery_terms_list", response_class=HTMLResponse)
async def delivery_terms_list(request: Request, session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    delivery_terms = await crud.get_delivery_terms_list_for_admin_page(session)
    delivery_terms = [term.model_dump() for term in delivery_terms]

    fields = list(DeliveryTermsForAdminList.model_fields.keys())
    link_fields = ["country_title", "city_title"]

    return templates.TemplateResponse(
        "pages/list.html",
        context={
            "request": request,
            "data": delivery_terms,
            "page title": "All Delivery Terms",
            "model_name": "Delivery Term",
            "fields": fields,
            "is_editable": True,
            "is_deletable": True,
            "link_fields": link_fields,
            "can_create": True
        }
    )


@router.get("/create", response_class=HTMLResponse)
async def create_delivery_term_page(request: Request,
                                    session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    form = DeliveryTermCreateForm()

    await set_countries_in_choices(session, form)
    await set_cities_in_choices(session, form)

    return templates.TemplateResponse(
        "pages/create.html",
        {
            "request": request,
            "form": form,
            "page_title": "Create Delivery Terms",
            "model_name": "Delivery Term"
        }
    )


@router.post("/create", name="admin_create_delivery_term", response_class=HTMLResponse)
async def create_delivery_term_submit(request: Request,
                                      session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    form_data = await request.form()
    form = DeliveryTermCreateForm(form_data)

    await set_countries_in_choices(session, form)
    await set_cities_in_choices(session, form)

    if form.validate():
        delivery_term_data = CreateDeliveryTerm(**form_data)

        delivery_term = await crud.create_delivery_term(session, delivery_term_data)
        return RedirectResponse(url=request.url_for("admin_delivery_terms_list"), status_code=status.HTTP_303_SEE_OTHER)

    return templates.TemplateResponse(
        "pages/create.html",
        {
            "request": request,
            "form": form,
            "page_title": "Create Delivery Term",
            "model_name": "Delivery Term"
        }
    )



@router.get("/{term_id}", response_class=HTMLResponse)
async def get_delivery_term_by_id(request: Request, term_id: int,
                                  session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    term = await crud.get_delivery_term_field_data(session, term_id)
    data = term.model_dump()

    return templates.TemplateResponse(
        "pages/detail.html",
        context={
            "request": request,
            "data": data,
            "page_title": "Delivery Terms",
            "model_name": "Delivery Term"
        }
    )


@router.get("/{delivery_term_id}/edit", response_class=HTMLResponse)
async def edit_delivery_term_by_id(request: Request, delivery_term_id: int,
                             session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    delivery_term = await crud.get_delivery_term_field_data(session, delivery_term_id)
    identifier = delivery_term.city_title or delivery_term.country_title

    form = DeliveryTermEditForm(data=delivery_term.model_dump())

    return templates.TemplateResponse(
        "pages/edit.html",
        {
            "request": request,
            "form": form,
            "page_title": "Edit Delivery Term",
            "model_name": "Delivery Term",
            "identifier": identifier
        }
    )


@router.post("/{term_id}/edit", name="admin_edit_delivery_terms", response_class=HTMLResponse)
async def edit_delivery_terms_submit(request: Request, term_id: int,
                              session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    form_data = await request.form()
    form = DeliveryTermEditForm(data=form_data)

    term = await crud.get_delivery_term_field_data(session, term_id)
    identifier = term.city_title or term.country_title

    if form.validate():
        term_data = EditDeliveryTerm(**form.data)
        await crud.update_delivery_term(session, term_id, term_data)

        return RedirectResponse(
            url=request.url_for("admin_edit_delivery_terms", term_id=term_id),
            status_code=status.HTTP_303_SEE_OTHER
        )

    return templates.TemplateResponse(
        "pages/edit.html",
        {
            "request": request,
            "form": form,
            "page_title": "Edit Delivery Term",
            "model_name": "Delivery Term",
            "identifier": identifier
        }
    )