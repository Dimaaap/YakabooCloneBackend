from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from core.models import db_helper
from .schema import CategoryForAdminList
from ..config import templates
from . import crud

router = APIRouter(tags=["Books Categories for Admin Page"])


@router.get("/list", response_class=HTMLResponse)
async def categories_list(request: Request, session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    categories = await crud.get_categories_for_admin_page(session)
    categories = [category.model_dump() for category in categories]
    fields = list(CategoryForAdminList.model_fields.keys())
    link_fields = ["subcategories_title", "banner_images"]

    return templates.TemplateResponse(
        "pages/categories/list.html",
        context={
            "request": request,
            "data": categories,
            "page_title": "All Categories",
            "model_name": "Category",
            "fields": fields,
            "is_editable": True,
            "is_deletable": True,
            "can_create": True,
            "link_fields": link_fields
        }
    )