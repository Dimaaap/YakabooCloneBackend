from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from core.models import db_helper
from .schema import BannersListForAdmin
from ..config import templates
from . import crud

router = APIRouter(tags=["Banners for Admin Page"])


@router.get("/list", response_class=HTMLResponse)
async def banners_list(request: Request, session: AsyncSession = Depends(db_helper.scoped_session_dependency)):

    banners = await crud.get_banners_for_admin_page(session)
    banners = [banner.model_dump() for banner in banners]
    fields = list(BannersListForAdmin.model_fields.keys())

    return templates.TemplateResponse(
        "pages/list.html",
        context={
            "request": request,
            "data": banners,
            "page_title": "All Banners",
            "model_name": "Banner",
            "fields": fields,
            "is_editable": True,
            "is_deletable": True,
            "can_create": True,
        }
    )