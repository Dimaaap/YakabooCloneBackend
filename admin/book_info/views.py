from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from core.models import db_helper
from .schema import BookInfoListForAdmin
from ..config import templates
from . import crud

router = APIRouter(tags=["Book Info List for Admin Page"])


@router.get("/list", response_class=HTMLResponse)
async def book_info_list(request: Request, session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    book_info = await crud.get_book_info_list_for_admin_page(session)
    book_info = [info.model_dump() for info in book_info]

    fields = list(BookInfoListForAdmin.model_fields.keys())
    link_fields = ["book_title"]

    return templates.TemplateResponse(
        "pages/book_info/list.html",
        context={
            "request": request,
            "data": book_info,
            "page_title": "All Book Info List",
            "model_name": "Book Info",
            "fields": fields,
            "is_editable": True,
            "is_deletable": True,
            "can_create": True,
            "link_fields": link_fields
        }
    )