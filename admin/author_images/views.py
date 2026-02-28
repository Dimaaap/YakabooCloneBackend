from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from core.models import db_helper
from .schema import AuthorImagesForAdminPage
from ..config import templates
from . import crud

router = APIRouter(tags=["Author Images For Admin Page"])


@router.get("/list", response_class=HTMLResponse)
async def author_images_list(request: Request, session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    author_images = await crud.get_author_images_for_admin_page(session)
    author_images = [image.model_dump() for image in author_images]

    fields = list(AuthorImagesForAdminPage.model_fields.keys())
    link_fields = ["author_name"]

    return templates.TemplateResponse(
        "pages/list.html",
        context={
            "request": request,
            "data": author_images,
            "page_title": "Author Images",
            "model_name": "Author Image",
            "fields": fields,
            "is_editable": True,
            "is_deletable": True,
            "can_create": True,
            "link_fields": link_fields
        }
    )

@router.get("/{author_image_id}", response_class=HTMLResponse)
async def get_author_image_by_id(request: Request, author_image_id: int,
                                 session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    author_image = await crud.get_author_image_field_data(session, author_image_id)
    data = author_image.model_dump()

    return templates.TemplateResponse(
        "pages/detail.html",
        context={
            "request": request,
            "data": data,
            "page_title": "Author Images",
            "model_name": "Author Image"
        }
    )