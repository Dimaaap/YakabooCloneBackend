from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from core.models import db_helper
from .schema import SidebarsForAdminPage
from ..config import templates
from . import crud

router = APIRouter(tags=["Sidebars For Admin Page"])


@router.get("/list", response_class=HTMLResponse)
async def get_sidebars(request: Request, session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    sidebars = await crud.get_sidebars_list_for_admin_page(session)
    sidebars = [sidebar.model_dump() for sidebar in sidebars]

    fields = list(SidebarsForAdminPage.model_fields.keys())

    return templates.TemplateResponse(
        "pages/sidebar/list.html",
        context={
            "request": request,
            "data": sidebars,
            "fields": fields,
            "page_title": "Sidebars",
            "model_name": "Sidebar",
            "is_editable": True,
            "is_deletable": True,
            "can_create": True
        }
    )



