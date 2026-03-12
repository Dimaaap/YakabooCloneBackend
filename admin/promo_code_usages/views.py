from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse

from core.models import db_helper
from .forms import PromoCodeUsageEditForm
from .schema import PromoCodeUsagesForAdmin, EditPromoCodeUsage
from ..config import templates
from . import crud
from ..utils import convert_alchemy_datetime

router = APIRouter(tags=["Promo Code Usages For Admin Page"])


@router.get("/list", response_class=HTMLResponse)
async def get_promo_code_usages(request: Request, session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    promo_code_usages = await crud.get_promo_code_usages_for_admin_page(session)
    promo_code_usages = [usage.model_dump() for usage in promo_code_usages]

    for usage in promo_code_usages:
        usage["used_at"] = convert_alchemy_datetime(usage["used_at"])

    fields = list(PromoCodeUsagesForAdmin.model_fields.keys())
    links_list = ["user_email", "promo_code_title"]

    return templates.TemplateResponse(
        "pages/list.html",
        context={
            "request": request,
            "data": promo_code_usages,
            "fields": fields,
            "page_title": "Promo Code Usages",
            "model_name": "Promo Code Usage",
            "is_editable": True,
            "is_deletable": True,
            "can_create": True,
            "link_fields": links_list
        }
    )


@router.get("/{usage_id}", response_class=HTMLResponse)
async def get_promo_code_usage_by_id(request: Request, usage_id: int,
                                     session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    usage = await crud.get_promo_code_usages_field_data(session, usage_id)
    data = usage.model_dump()

    return templates.TemplateResponse(
        "pages/detail.html",
        context={
            "request": request,
            "data": data,
            "page_title": "Promo Code Usages",
            "model_name": "Promo Code Usage"
        }
    )


@router.get("/{usage_id}/edit", response_class=HTMLResponse)
async def edit_promo_code_usage_by_id(request: Request, usage_id: int,
                            session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    usage = await crud.get_promo_code_usages_field_data(session, usage_id)

    identifier = f"{usage.promo_code_title} - {usage.user_email}"

    form = PromoCodeUsageEditForm(data=usage.model_dump())

    return templates.TemplateResponse(
        "pages/edit.html",
        context={
            "request": request,
            "form": form,
            "page_title": "Edit Promo Code Usage",
            "model_name": "Promo Code Usage",
            "identifier": identifier
        }
    )


@router.post("/{usage_id}/edit", name="admin_edit_promo_code_usage", response_class=HTMLResponse)
async def edit_promo_category_submit(request: Request, usage_id: int,
                                session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    form_data = await request.form()
    form = PromoCodeUsageEditForm(data=form_data)

    promo_usage = await crud.get_promo_code_usages_field_data(session, usage_id)
    identifier = f"{promo_usage.promo_code_title} - {promo_usage.user_email}"

    if form.validate():
        promo_usage_data = EditPromoCodeUsage(**form.data)
        await crud.update_promo_code_usage(session, usage_id, promo_usage_data)

        return RedirectResponse(
            url=request.url_for("admin_edit_promo_code_usage", usage_id=usage_id),
            status_code=status.HTTP_303_SEE_OTHER
        )

    return templates.TemplateResponse(
        "pages/edit.html",
        {
            "request": request,
            "form": form,
            "page_title": "Edit Promo Code Usage",
            "model_name": "Promo Code Usage",
            "identifier": identifier
        }
    )
