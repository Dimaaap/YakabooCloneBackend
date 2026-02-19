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
        "pages/contacts/list.html",
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