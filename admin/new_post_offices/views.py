from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse

from core.models import db_helper
from .forms import NewPostOfficeEditForm, NewPostOfficeCreateForm
from .schema import NewPostOfficesForAdmin, EditNewPostOffice, CreateNewPostOffice
from ..config import templates
from . import crud

router = APIRouter(tags=["New Post Offices for Admin Page"])


@router.get("/list", name="admin_new_post_offices_list", response_class=HTMLResponse)
async def get_new_post_offices(request: Request, session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    new_post_offices = await crud.get_new_post_offices_for_admin_page(session)
    new_post_offices = [office.model_dump() for office in new_post_offices]

    fields = list(NewPostOfficesForAdmin.model_fields.keys())
    link_fields = ["city_title"]

    return templates.TemplateResponse(
        "pages/list.html",
        context={
            "request": request,
            "data": new_post_offices,
            "page_title": "New Post Offices",
            "model_name": "New Post Office",
            "fields": fields,
            "is_editable": True,
            "is_deletable": True,
            "can_create": True,
            "link_fields": link_fields,
        }
    )


@router.get("/create", response_class=HTMLResponse)
async def create_new_post_office_page(request: Request,
                                      session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    form = NewPostOfficeCreateForm()

    await crud.set_cities_in_choices(session, form)

    return templates.TemplateResponse(
        "pages/create.html",
        {
            "request": request,
            "form": form,
            "page_title": "Create New Post Office",
            "model_name": "New Post Office",
        }
    )


@router.post("/create", response_class=HTMLResponse)
async def create_new_post_office_submit(request: Request,
                                        session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    form_data = await request.form()
    form = NewPostOfficeCreateForm(form_data)

    await crud.set_cities_in_choices(session, form)

    if form.validate():
        office_data = CreateNewPostOffice(**form.data)
        _ = await crud.create_new_post_office(session, office_data)

        return RedirectResponse(
            url=request.url_for("admin_new_post_offices_list"),
            status_code=status.HTTP_303_SEE_OTHER
        )

    return templates.TemplateResponse(
        "pages/create.html",
        {
            "request": request,
            "form": form,
            "page_title": "Create New Post Office",
            "model_name": "New Post Office"
        }
    )


@router.get("/{office_id}", response_class=HTMLResponse)
async def get_new_post_office_by_id(request: Request, office_id: int,
                                    session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    office = await crud.get_new_post_offices_field_data(session, office_id)
    data = office.model_dump()

    return templates.TemplateResponse(
        "pages/detail.html",
        context={
            "request": request,
            "data": data,
            "page_title": "New Post Offices",
            "model_name": "New Post Office"
        }
    )


@router.get("/{office_id}/edit", response_class=HTMLResponse)
async def edit_new_post_office_by_id(request: Request, office_id: int,
                            session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    office = await crud.get_new_post_offices_field_data(session, office_id)

    identifier = office.number

    form = NewPostOfficeEditForm(data=office.model_dump())

    return templates.TemplateResponse(
        "pages/edit.html",
        context={
            "request": request,
            "form": form,
            "page_title": "Edit New Post Office",
            "model_name": "New Post Office",
            "identifier": identifier
        }
    )


@router.post("/{office_id}/edit", name="admin_edit_new_post_office", response_class=HTMLResponse)
async def edit_new_post_office_submit(request: Request, office_id: int,
                                session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    form_data = await request.form()
    form = NewPostOfficeEditForm(data=form_data)

    office = await crud.get_new_post_offices_field_data(session, office_id)
    identifier = office.number

    if form.validate():
        office_data = EditNewPostOffice(**form.data)
        await crud.update_new_post_office(session, office_id, office_data)

        return RedirectResponse(
            url=request.url_for("admin_edit_new_post_office", office_id=office_id),
            status_code=status.HTTP_303_SEE_OTHER
        )

    return templates.TemplateResponse(
        "pages/edit.html",
        {
            "request": request,
            "form": form,
            "page_title": "Edit New Post Office",
            "model_name": "New Post Office",
            "identifier": identifier
        }
    )