from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse

from core.models import db_helper
from .forms import PromoCodesEditForm, PromoCodeCreateForm
from .schema import PromoCodesAdminList, EditPromoCode, CreatePromoCode
from ..config import templates
from . import crud
from ..utils import convert_alchemy_datetime

router = APIRouter(tags=["Promo Codes For Admin Page"])


@router.get("/list", name="admin_promo_codes_list", response_class=HTMLResponse)
async def get_promo_codes(request: Request, session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    promo_codes = await crud.get_promo_codes_for_admin_page(session)
    promo_codes = [code.model_dump() for code in promo_codes]

    for code in promo_codes:
        code["expires_at"] = convert_alchemy_datetime(code["expires_at"])

    fields = list(PromoCodesAdminList.model_fields.keys())

    return templates.TemplateResponse(
        "pages/list.html",
        context={
            "request": request,
            "data": promo_codes,
            "fields": fields,
            "page_title": "Promo Codes",
            "model_name": "Promo Code",
            "is_editable": True,
            "is_deletable": True,
            "can_create": True,
        }
    )


@router.get("/create", response_class=HTMLResponse)
async def create_promo_code_page(request: Request):
    form = PromoCodeCreateForm()

    return templates.TemplateResponse(
        "pages/create.html",
        {
            "request": request,
            "form": form,
            "page_title": "Create Promo Code",
            "model_name": "Promo Code"
        }
    )


@router.post("/create", response_class=HTMLResponse)
async def create_promo_code_submit(request: Request,
                                   session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    form_data = await request.form()

    form = PromoCodeCreateForm(form_data)

    if form.validate():
        promo_code = CreatePromoCode(**form.data)
        _ = await crud.create_promo_code(session, promo_code)

        return RedirectResponse(
            url=request.url_for("admin_promo_codes_list"),
            status_code=status.HTTP_303_SEE_OTHER
        )

    return templates.TemplateResponse(
        "pages/create.html",
        {
            "request": request,
            "form": form,
            "page_title": "Create Promo Code",
            "model_name": "Promo Code"
        }
    )


@router.get("/{promo_code_id}", response_class=HTMLResponse)
async def get_promo_code_by_id(request: Request, promo_code_id: int,
                               session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    promo_code = await crud.get_promo_codes_field_data(session, promo_code_id)
    data = promo_code.model_dump()

    return templates.TemplateResponse(
        "pages/detail.html",
        context={
            "request": request,
            "data": data,
            "page_title": "Promo Codes",
            "model_name": "Promo Code"
        }
    )


@router.get("/{promo_code_id}/edit", response_class=HTMLResponse)
async def edit_promo_code_by_id(request: Request, promo_code_id: int,
                            session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    promo_code = await crud.get_promo_codes_field_data(session, promo_code_id)

    identifier = promo_code.code

    form = PromoCodesEditForm(data=promo_code.model_dump())

    return templates.TemplateResponse(
        "pages/edit.html",
        context={
            "request": request,
            "form": form,
            "page_title": "Edit Promo Code",
            "model_name": "Promo Code",
            "identifier": identifier
        }
    )


@router.post("/{promo_code_id}/edit", name="admin_edit_promo_code", response_class=HTMLResponse)
async def edit_promo_code_submit(request: Request, promo_code_id: int,
                                session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    form_data = await request.form()
    form = PromoCodesEditForm(data=form_data)

    promo_code = await crud.get_promo_codes_field_data(session, promo_code_id)
    identifier = promo_code.code

    if form.validate():
        category_data = EditPromoCode(**form.data)
        await crud.update_promo_code(session, promo_code_id, category_data)

        return RedirectResponse(
            url=request.url_for("admin_edit_promo_code", promo_code_id=promo_code_id),
            status_code=status.HTTP_303_SEE_OTHER
        )

    return templates.TemplateResponse(
        "pages/edit.html",
        {
            "request": request,
            "form": form,
            "page_title": "Edit Promo Code",
            "model_name": "Promo Code",
            "identifier": identifier
        }
    )
