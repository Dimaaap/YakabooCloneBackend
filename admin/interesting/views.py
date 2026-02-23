from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from core.models import db_helper
from .schema import InterestingForAdminList
from ..config import templates
from . import crud

router = APIRouter(tags=["Admin Interesting"])


@router.get("/list", response_class=HTMLResponse)
async def interesting_list(request: Request, session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    all_interesting = await crud.get_interesting_list_for_admin_page(session)
    all_interesting = [interesting.model_dump() for interesting in all_interesting]

    fields = list(InterestingForAdminList.model_fields.keys())

    return templates.TemplateResponse(
        "pages/interesting/list.html",
        context={
            "request": request,
            "data": all_interesting,
            "page_title": "All interesting",
            "model_name": "Interesting",
            "fields": fields,
            "is_editable": True,
            "is_deletable": True,
            "can_create": True,
        }
    )