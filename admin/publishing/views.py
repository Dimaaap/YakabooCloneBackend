from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from core.models import db_helper
from .schema import PublishingListForAdmin
from ..config import templates
from . import crud

router = APIRouter(tags=["Publishing List For Admin"])


@router.get("/list", response_class=HTMLResponse)
async def get_publishing_list(request: Request, session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    publishing_list = await crud.get_publishing_list_for_admin_page(session)
    publishing_list = [publishing.model_dump() for publishing in publishing_list]

    fields = list(PublishingListForAdmin.model_fields.keys())

    return templates.TemplateResponse(
        "pages/list.html",
        context={
            "request": request,
            "data": publishing_list,
            "fields": fields,
            "page_title": "Publishing List",
            "model_name": "Publishing",
            "is_editable": True,
            "is_deletable": True,
            "can_create": True,
        }
    )