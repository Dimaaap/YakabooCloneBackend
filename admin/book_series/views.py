from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from core.models import db_helper
from .schema import BookSeriesForAdminList
from ..config import templates
from . import crud

router = APIRouter(tags=["Book Series for Admin Page"])


@router.get("/list", response_class=HTMLResponse)
async def series_list(request: Request, session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    series = await crud.get_book_series_for_admin_page(session)
    series = [seria.model_dump() for seria in series]

    fields = list(BookSeriesForAdminList.model_fields.keys())

    return templates.TemplateResponse(
        "pages/list.html",
        context={
            "request": request,
            "data": series,
            "page_title": "All Book Series",
            "model_name": "Book Seria",
            "fields": fields,
            "is_editable": True,
            "is_deletable": True,
            "can_create": True,
        }
    )
