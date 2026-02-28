from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from core.models import db_helper
from .schema import ContactsForAdminList
from ..config import templates
from . import crud

router = APIRouter(tags=["Contacts for Admin Page"])


@router.get("/list", response_class=HTMLResponse)
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