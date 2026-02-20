from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from core.models import db_helper
from .schema import DoubleSubcategoriesForAdminList
from ..config import templates
from . import crud

router = APIRouter(tags=["Admin Double Subcategories"])


@router.get("/list", response_class=HTMLResponse)
async def double_subcategories_list(request: Request, session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    double_subcategories = await crud.get_double_subcategories_for_admin_page(session)
    double_subcategories = [subcategory.model_dump() for subcategory in double_subcategories]

    fields = list(DoubleSubcategoriesForAdminList.model_fields.keys())
    link_fields = ["subcategory_title"]

    return templates.TemplateResponse(
        "pages/double_subcategories/list.html",
        context={
            "request": request,
            "data": double_subcategories,
            "page_title": "All Double Subcategories",
            "model_name": "Double Subcategory",
            "fields": fields,
            "is_editable": True,
            "is_deletable": True,
            "can_create": True,
            "link_fields": link_fields,
        }
    )