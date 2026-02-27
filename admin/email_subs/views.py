from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from core.models import db_helper
from .schema import EmailSubsForAdminList
from ..config import templates
from . import crud
from ..utils import convert_alchemy_datetime

router = APIRouter(tags=["Email Subs For Admin"])


@router.get("/list", response_class=HTMLResponse)
async def get_email_subs_list(request: Request, session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    email_subs = await crud.get_admin_subs_for_admin_page(session)
    email_subs = [sub.model_dump() for sub in email_subs]

    for sub in email_subs:
        sub["date_sub"] = convert_alchemy_datetime(sub["date_sub"])

    fields = list(EmailSubsForAdminList.model_fields.keys())

    return templates.TemplateResponse(
        "pages/list.html",
        context={
            "request": request,
            "data": email_subs,
            "page_title": "All Email Subs",
            "model_name": "Email Sub",
            "fields": fields,
            "is_editable": True,
            "is_deletable": True,
            "can_create": True,
        }
    )

