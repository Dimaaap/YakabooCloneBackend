from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse

from core.models import db_helper
from .forms import LiteraturePeriodsEditForm
from .schema import LiteraturePeriodForAdminList, EditLiteraturePeriod
from ..config import templates
from . import crud

router = APIRouter(tags=["Literature Periods for Admin"])


@router.get("/list", response_class=HTMLResponse)
async def literature_periods_list(request: Request,
                                  session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    literature_periods = await crud.get_literature_periods_for_admin_page(session)
    literature_periods = [period.model_dump() for period in literature_periods]

    fields = list(LiteraturePeriodForAdminList.model_fields.keys())

    return templates.TemplateResponse(
        "pages/list.html",
        context={
            "request": request,
            "data": literature_periods,
            "page_title": "All Literature Periods",
            "model_name": "Literature Period",
            "fields": fields,
            "is_editable": True,
            "is_deletable": True,
            "can_create": True,
        }
    )


@router.get("/{literature_period_id}", response_class=HTMLResponse)
async def get_literature_period_by_id(request: Request, literature_period_id: int,
                                      session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    literature_period = await crud.get_literature_period_field_data(session, literature_period_id)
    data = literature_period.model_dump()

    return templates.TemplateResponse(
        "pages/detail.html",
        context={
            "request": request,
            "data": data,
            "page_title": "Literature Periods",
            "model_name": "Literature Period"
        }
    )


@router.get("/{period_id}/edit", response_class=HTMLResponse)
async def edit_interesting_by_id(request: Request, period_id: int,
                            session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    literature_period = await crud.get_literature_period_field_data(session, period_id)

    identifier = literature_period.title

    form = LiteraturePeriodsEditForm(data=literature_period.model_dump())

    return templates.TemplateResponse(
        "pages/edit.html",
        context={
            "request": request,
            "form": form,
            "page_title": "Edit Literature Period",
            "model_name": "Literature Period",
            "identifier": identifier
        }
    )


@router.post("/{period_id}/edit", name="admin_edit_literature_period", response_class=HTMLResponse)
async def edit_literature_period_submit(request: Request, period_id: int,
                                session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    form_data = await request.form()
    form = LiteraturePeriodsEditForm(data=form_data)

    literature_period = await crud.get_literature_period_field_data(session, period_id)
    identifier = literature_period.title

    if form.validate():
        period_data = EditLiteraturePeriod(**form.data)
        await crud.update_literature_period(session, period_id, period_data)

        return RedirectResponse(
            url=request.url_for("admin_edit_literature_period", period_id=period_id),
            status_code=status.HTTP_303_SEE_OTHER
        )

    return templates.TemplateResponse(
        "pages/edit.html",
        {
            "request": request,
            "form": form,
            "page_title": "Edit Literature Period",
            "model_name": "Literature Period",
            "identifier": identifier
        }
    )