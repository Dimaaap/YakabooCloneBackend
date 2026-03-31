from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse

from core.models import db_helper
from entities.meest_post_offices.schema import MeestPostOfficeCreate
from .forms import MeestPostOfficeEditForm, MeestPostOfficeCreateForm
from .schema import MeestPostOfficesForAdmin, EditMeestPostOffice, CreateMeestPostOffice
from ..config import templates
from . import crud

router = APIRouter(tags=["Meest Post Offices for Admin Page"])


@router.get("/list", name="admin_meest_post_offices_list", response_class=HTMLResponse)
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


@router.get("/create", response_class=HTMLResponse)
async def create_meest_post_office_page(request: Request,
                                        session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    form = MeestPostOfficeCreateForm()

    await crud.set_cities_in_choices(session, form)

    return templates.TemplateResponse(
        "pages/create.html",
        {
            "request": request,
            "form": form,
            "page_title": "Create Meest Post Office",
            "model_name": "Meest Post Office"
        }
    )


@router.post("/create", response_class=HTMLResponse)
async def create_meest_post_office_submit(request: Request,
                                          session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    form_data = await request.form()
    form = MeestPostOfficeCreateForm(form_data)

    await crud.set_cities_in_choices(session, form)

    if form.validate():
        office_data = CreateMeestPostOffice(**form.data)
        _ = await crud.create_meest_post_office(session, office_data)

        return RedirectResponse(
            url=request.url_for("admin_meest_post_offices_list"),
            status_code=status.HTTP_303_SEE_OTHER
        )

    return templates.TemplateResponse(
        "pages/create.html",
        {
            "request": request,
            "form": form,
            "page_title": "Create Meest Post Office",
            "model_name": "Meest Post Office"
        }
    )



@router.get("/{office_id}", response_class=HTMLResponse)
async def get_meest_post_office_by_id(request: Request, office_id: int,
                                      session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    office = await crud.get_meest_post_offices_field_data(session, office_id)
    data = office.model_dump()

    return templates.TemplateResponse(
        "pages/detail.html",
        context={
            "request": request,
            "data": data,
            "page_title": "Meest Post Offices",
            "model_name": "Meest Post Office"
        }
    )


@router.get("/{office_id}/edit", response_class=HTMLResponse)
async def edit_interesting_by_id(request: Request, office_id: int,
                            session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    office = await crud.get_meest_post_offices_field_data(session, office_id)

    identifier = office.office_number

    form = MeestPostOfficeEditForm(data=office.model_dump())

    return templates.TemplateResponse(
        "pages/edit.html",
        context={
            "request": request,
            "form": form,
            "page_title": "Edit Meest Post Office",
            "model_name": "Meest Post Office",
            "identifier": identifier
        }
    )


@router.post("/{office_id}/edit", name="admin_edit_meest_post_office", response_class=HTMLResponse)
async def edit_meest_post_office_submit(request: Request, office_id: int,
                                session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    form_data = await request.form()
    form = MeestPostOfficeEditForm(data=form_data)

    office = await crud.get_meest_post_offices_field_data(session, office_id)
    identifier = office.office_number

    if form.validate():
        office_data = EditMeestPostOffice(**form.data)
        await crud.update_meest_post_office(session, office_id, office_data)

        return RedirectResponse(
            url=request.url_for("admin_edit_meest_post_office", office_id=office_id),
            status_code=status.HTTP_303_SEE_OTHER
        )

    return templates.TemplateResponse(
        "pages/edit.html",
        {
            "request": request,
            "form": form,
            "page_title": "Edit Meest Post Office",
            "model_name": "Meest Post Office",
            "identifier": identifier
        }
    )