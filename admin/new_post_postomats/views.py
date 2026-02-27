from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from core.models import db_helper
from .schema import NewPostPostomatsForAdmin
from ..config import templates
from . import crud

router = APIRouter(tags=["New Post Postomats for Admin Page"])


@router.get("/list", response_class=HTMLResponse)
async def get_new_post_offices(request: Request, session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    new_post_postomats = await crud.get_new_post_postomats_for_admin_page(session)
    new_post_postomats = [postomat.model_dump() for postomat in new_post_postomats]

    fields = list(NewPostPostomatsForAdmin.model_fields.keys())
    link_fields = ["city_title"]

    return templates.TemplateResponse(
        "pages/list.html",
        context={
            "request": request,
            "data": new_post_postomats,
            "page_title": "New Post Postomats",
            "model_name": "New Post Postomat",
            "fields": fields,
            "is_editable": True,
            "is_deletable": True,
            "can_create": True,
            "link_fields": link_fields,
        }
    )