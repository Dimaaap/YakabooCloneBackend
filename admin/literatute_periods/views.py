from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from core.models import db_helper
from .schema import LiteraturePeriodForAdminList
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