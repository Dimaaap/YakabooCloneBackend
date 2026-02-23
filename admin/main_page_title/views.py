from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from core.models import db_helper
from .schema import MainPageTitlesListForAdmin
from ..config import templates
from . import crud
from ..utils import convert_alchemy_datetime

router = APIRouter(tags=["Main Page Titles for Admin"])


@router.get("/list", response_class=HTMLResponse)
async def get_main_page_titles(request: Request, session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    main_page_titles = await crud.get_main_page_titles_for_admin_page(session)
    main_page_titles = [title.model_dump() for title in main_page_titles]

    for title in main_page_titles:
        title["created_at"] = convert_alchemy_datetime(title["created_at"])
        title["updated_at"] = convert_alchemy_datetime(title["updated_at"])

    fields = list(MainPageTitlesListForAdmin.model_fields.keys())

    return templates.TemplateResponse(
        "pages/main_page_titles/list.html",
        context={
            "request": request,
            "data": main_page_titles,
            "page_title": "All Main Page Titles",
            "model_name": "Main Page Title",
            "fields": fields,
            "is_editable": True,
            "is_deletable": True,
            "can_create": True,
        }
    )