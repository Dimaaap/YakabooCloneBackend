from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from core.models import db_helper
from .schema import NewPostOfficesForAdmin
from ..config import templates
from . import crud

router = APIRouter(tags=["New Post Offices for Admin Page"])


@router.get("/list", response_class=HTMLResponse)
async def get_new_post_offices(request: Request, session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    new_post_offices = await crud.get_new_post_offices_for_admin_page(session)
    new_post_offices = [office.model_dump() for office in new_post_offices]

    fields = list(NewPostOfficesForAdmin.model_fields.keys())
    link_fields = ["city_title"]

    return templates.TemplateResponse(
        "pages/list.html",
        context={
            "request": request,
            "data": new_post_offices,
            "page_title": "New Post Offices",
            "model_name": "New Post Office",
            "fields": fields,
            "is_editable": True,
            "is_deletable": True,
            "can_create": True,
            "link_fields": link_fields,
        }
    )