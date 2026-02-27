from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from core.models import db_helper
from .schema import BooksForAdminList
from ..config import templates
from . import crud
from ..utils import convert_alchemy_datetime

router = APIRouter(tags=["Books For Admin Page"])


@router.get("/list", response_class=HTMLResponse)
async def books_list(request: Request, session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    books = await crud.get_books_for_admin_page(session)
    books = [book.model_dump() for book in books]

    for book in books:
        book["created_date"] = convert_alchemy_datetime(book["created_date"])

    fields = list(BooksForAdminList.model_fields.keys())
    link_fields = ["book_info_id", "authors_names", "translators_names",
                   "illustrators_names", "literature_period_title",
                   "book_seria_title", "notebook_category_title",
                   "notebook_subcategory_title", "subcategories_title",
                   "categories_title", "double_subcategories_title",
                   "publishing_title", "edition_group_title",
                   "book_images"]

    return templates.TemplateResponse(
        "pages/list.html",
        context={
            "request": request,
            "data": books,
            "page_title": "All Books",
            "model_name": "Book",
            "fields": fields,
            "is_editable": True,
            "is_deletable": True,
            "can_create": True,
            "link_fields": link_fields,
        }
    )