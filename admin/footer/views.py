from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from core.models import db_helper
from .schema import FooterForAdminList
from ..config import templates
from . import crud

router = APIRouter(tags=["Footers For Admin"])


@router.get("/list", response_class=HTMLResponse)
async def get_email_subs_list(request: Request, session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    footers = await crud.get_footers_for_admin_page(session)
    footers = [footer.model_dump() for footer in footers]

    fields = list(FooterForAdminList.model_fields.keys())

    return templates.TemplateResponse(
        "pages/footers/list.html",
        context={
            "request": request,
            "data": footers,
            "page_title": "All Footers",
            "model_name": "Footer",
            "fields": fields,
            "is_editable": True,
            "is_deletable": True,
            "can_create": True,
        }
    )

