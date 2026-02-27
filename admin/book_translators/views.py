from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from core.models import db_helper
from .schema import BookTranslatorsListForAdminPage
from ..config import templates
from . import crud

router = APIRouter(tags=["Book Translators for Admin Page"])


@router.get("/list", response_class=HTMLResponse)
async def series_list(request: Request, session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    series = await crud.get_book_translators_for_admin_page(session)
    series = [seria.model_dump() for seria in series]

    fields = list(BookTranslatorsListForAdminPage.model_fields.keys())

    return templates.TemplateResponse(
        "pages/list.html",
        context={
            "request": request,
            "data": series,
            "page_title": "All Book Translators",
            "model_name": "Book Translator",
            "fields": fields,
            "is_editable": True,
            "is_deletable": True,
            "can_create": True,
        }
    )
