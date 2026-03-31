from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse

from core.models import db_helper
from .forms import PaymentMethodEditForm, PaymentMethodCreateForm
from .schema import PaymentMethodsForAdmin, EditPaymentMethod, CreatePaymentMethod
from ..config import templates
from . import crud

router = APIRouter(tags=["Payment Methods For Admin"])


@router.get("/list", name="admin_payment_methods_list", response_class=HTMLResponse)
async def get_payment_methods(request: Request, session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    payment_methods = await crud.get_payment_methods_for_admin_page(session)
    payment_methods = [method.model_dump() for method in payment_methods]

    fields = list(PaymentMethodsForAdmin.model_fields.keys())
    link_fields = ["country_title", "city_title"]

    return templates.TemplateResponse(
        "pages/list.html",
        context={
            "request": request,
            "data": payment_methods,
            "page_title": "Payment Methods",
            "model_name": "Payment Method",
            "fields": fields,
            "is_editable": True,
            "is_deletable": True,
            "can_create": True,
            "link_fields": link_fields,
        }
    )


@router.get("/create", response_class=HTMLResponse)
async def create_payment_method(request: Request,
                                session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    form = PaymentMethodCreateForm()

    await crud.set_countries_in_choices(session, form)
    await crud.set_cities_in_choices(session, form)

    return templates.TemplateResponse(
        "pages/create.html",
        {
            "request": request,
            "form": form,
            "page_title": "Create Payment Method",
            "model_name": "Payment Method"
        }
    )


@router.post("/create", response_class=HTMLResponse)
async def create_payment_method_submit(request: Request,
                                       session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    form_data = await request.form()
    form = PaymentMethodCreateForm(form_data)

    await crud.set_cities_in_choices(session, form)
    await crud.set_countries_in_choices(session, form)

    if form.validate():
        payment_method_data = CreatePaymentMethod(**form.data)
        _ = await crud.create_payment_method(session, payment_method_data)

        return RedirectResponse(
            url=request.url_for("admin_payment_methods_list"),
            status_code=status.HTTP_303_SEE_OTHER
        )

    return templates.TemplateResponse(
        "pages/create.html",
        {
            "request": request,
            "form": form,
            "page_title": "Create Payment Method",
            "model_name": "Payment Method"
        }
    )


@router.get("/{payment_id}", response_class=HTMLResponse)
async def get_payment_method_by_id(request: Request, payment_id: int,
                                   session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    method = await crud.get_payment_methods_field_data(session, payment_id)
    data = method.model_dump()

    return templates.TemplateResponse(
        "pages/detail.html",
        context={
            "request": request,
            "data": data,
            "page_title": "Payment Methods",
            "model_name": "Payment Method"
        }
    )


@router.get("/{method_id}/edit", response_class=HTMLResponse)
async def edit_postomat_by_id(request: Request, method_id: int,
                            session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    payment_method = await crud.get_payment_methods_field_data(session, method_id)

    identifier = payment_method.id

    form = PaymentMethodEditForm(data=payment_method.model_dump())

    return templates.TemplateResponse(
        "pages/edit.html",
        context={
            "request": request,
            "form": form,
            "page_title": "Edit Payment Method",
            "model_name": "Payment Method",
            "identifier": identifier
        }
    )


@router.post("/{method_id}/edit", name="admin_edit_payment_method", response_class=HTMLResponse)
async def edit_payment_method_submit(request: Request, method_id: int,
                                session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    form_data = await request.form()
    form = PaymentMethodEditForm(data=form_data)

    payment_method = await crud.get_payment_methods_field_data(session, method_id)
    identifier = payment_method.id

    if form.validate():
        office_data = EditPaymentMethod(**form.data)
        await crud.update_payment_method(session, method_id, office_data)

        return RedirectResponse(
            url=request.url_for("admin_edit_payment_method", method_id=method_id),
            status_code=status.HTTP_303_SEE_OTHER
        )

    return templates.TemplateResponse(
        "pages/edit.html",
        {
            "request": request,
            "form": form,
            "page_title": "Edit Payment Method",
            "model_name": "Payment Method",
            "identifier": identifier
        }
    )

