from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse

from core.models import db_helper
from .forms import BannerEditForm
from .schema import BannersListForAdmin, EditBanner
from ..config import templates
from . import crud

router = APIRouter(tags=["Banners for Admin Page"])


@router.get("/list", response_class=HTMLResponse)
async def banners_list(request: Request, session: AsyncSession = Depends(db_helper.scoped_session_dependency)):

    banners = await crud.get_banners_for_admin_page(session)
    banners = [banner.model_dump() for banner in banners]
    fields = list(BannersListForAdmin.model_fields.keys())

    return templates.TemplateResponse(
        "pages/list.html",
        context={
            "request": request,
            "data": banners,
            "page_title": "All Banners",
            "model_name": "Banner",
            "fields": fields,
            "is_editable": True,
            "is_deletable": True,
            "can_create": True,
        }
    )


@router.get("/{banner_id}", response_class=HTMLResponse)
async def get_banner_by_id(request: Request, banner_id: int,
                           session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    banner = await crud.get_banner_field_data(session, banner_id)
    data = banner.model_dump()

    return templates.TemplateResponse(
        "pages/detail.html",
        context={
            "request": request,
            "data": data,
            "page_title": "Banners",
            "model_name": "Banner"
        }
    )


@router.get("/{banner_id}/edit", response_class=HTMLResponse)
async def edit_banner_by_id(request: Request, banner_id: int,
                            session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    banner = await crud.get_banner_field_data(session, banner_id)

    identifier = banner.link

    form = BannerEditForm(data=banner.model_dump())

    return templates.TemplateResponse(
        "pages/edit.html",
        {
            "request": request,
            "form": form,
            "page_title": "Edit Banner",
            "model_name": "Banner",
            "identifier": identifier
        }
    )


@router.post("/{banner_id}/edit", name="admin_edit_banner", response_class=HTMLResponse)
async def edit_banner_submit(request: Request, banner_id: int,
                             session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    form_data = await request.form()
    form = BannerEditForm(form_data)

    banner = await crud.get_banner_field_data(session, banner_id)
    identifier = banner.link

    if form.validate():
        banner_data = EditBanner(**form.data)
        await crud.update_banner(session, banner_id, banner_data)

        return RedirectResponse(
            url=request.url_for("admin_edit_banner", banner_id=banner_id),
            status_code=status.HTTP_303_SEE_OTHER
        )

    return templates.TemplateResponse(
        "pages/edit.html",
        {
            "request": request,
            "form": form,
            "page_title": "Edit Banner",
            "model_name": "Banner",
            "identifier": identifier
        }
    )