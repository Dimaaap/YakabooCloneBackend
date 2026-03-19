from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse

from core.models import db_helper
from .forms import ContactEditForm, ContactCreateForm
from .schema import ContactsForAdminList, EditContacts, CreateContacts
from ..config import templates
from . import crud

router = APIRouter(tags=["Contacts for Admin Page"])


@router.get("/list", name="admin_contacts_list", response_class=HTMLResponse)
async def contacts_list(request: Request, session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    contacts = await crud.get_contacts_list_for_admin_page(session)
    contacts = [contact.model_dump() for contact in contacts]
    fields = list(ContactsForAdminList.model_fields.keys())

    return templates.TemplateResponse(
        "pages/list.html",
        context={
            "request": request,
            "data": contacts,
            "page_title": "All Contacts",
            "model_name": "Contact",
            "fields": fields,
            "is_editable": True,
            "is_deletable": True,
            "can_create": True,
        }
    )


@router.get("/create", response_class=HTMLResponse)
async def create_contact_page(request: Request):
    form = ContactCreateForm()

    return templates.TemplateResponse(
        "pages/create.html",
        {
            "request": request,
            "form": form,
            "page_title": "Create Contact",
            "model_name": "Contact"
        }
    )


@router.post("/create", name="admin_create_contact", response_class=HTMLResponse)
async def create_contact_submit(request: Request, session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    form_data = await request.form()
    form = ContactCreateForm(form_data)

    if form.validate():
        contact_data = CreateContacts(**form.data)
        await crud.create_contact(session, contact_data)

        return RedirectResponse(
            url=request.url_for("admin_contacts_list"),
            status_code=status.HTTP_303_SEE_OTHER
        )

    return templates.TemplateResponse(
        "pages/create.html",
        {
            "request": request,
            "form": form,
            "page_title": "Create Contact",
            "model_name": "Contact"
        }
    )


@router.get("/{contact_id}", response_class=HTMLResponse)
async def get_contact_by_id(request: Request, contact_id: int,
                            session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    contact = await crud.get_contact_field_data(session, contact_id)

    data = contact.model_dump()

    return templates.TemplateResponse(
        "pages/detail.html",
        context={
            "request": request,
            "data": data,
            "page_title": "Contacts",
            "model_name": "Contact"
        }
    )


@router.get("/{contact_id}/edit", response_class=HTMLResponse)
async def edit_contact_by_id(request: Request, contact_id: int,
                             session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    contact = await crud.get_contact_field_data(session, contact_id)
    identifier = contact.social_title

    form = ContactEditForm(data=contact.model_dump())

    return templates.TemplateResponse(
        "pages/edit.html",
        {
            "request": request,
            "form": form,
            "page_title": "Edit Contact",
            "model_name": "Contact",
            "identifier": identifier
        }
    )


@router.post("/{contact_id}/edit", name="admin_edit_contacts", response_class=HTMLResponse)
async def edit_contacts_submit(request: Request, contact_id: int,
                              session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    form_data = await request.form()
    form = ContactEditForm(data=form_data)

    contact = await crud.get_contact_field_data(session, contact_id)
    identifier = contact.social_title

    if form.validate():
        contact_data = EditContacts(**form.data)
        await crud.update_contact(session, contact_id, contact_data)

        return RedirectResponse(
            url=request.url_for("admin_edit_contacts", contact_id=contact_id),
            status_code=status.HTTP_303_SEE_OTHER
        )

    return templates.TemplateResponse(
        "pages/edit.html",
        {
            "request": request,
            "form": form,
            "page_title": "Edit Contact",
            "model_name": "Contact",
            "identifier": identifier
        }
    )