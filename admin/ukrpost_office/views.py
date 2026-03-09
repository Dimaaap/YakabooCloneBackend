from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from core.models import db_helper
from .forms import UkrpostOfficeEditForm
from .schema import UkrpostOfficesForAdmin
from ..config import templates
from . import crud

router = APIRouter(tags=["Ukrpost Offices For Admin Page"])


@router.get("/list", response_class=HTMLResponse)
async def get_ukrpost_offices(request: Request, session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    ukrpost_offices = await crud.get_ukrpost_offices_for_admin_page(session)
    ukrpost_offices = [office.model_dump() for office in ukrpost_offices]

    fields = list(UkrpostOfficesForAdmin.model_fields.keys())
    link_fields = ["city_title"]

    return templates.TemplateResponse(
        "pages/list.html",
        context={
            "request": request,
            "data": ukrpost_offices,
            "page_title": "Ukrpost Offices",
            "model_name": "Ukrpost Office",
            "fields": fields,
            "is_editable": True,
            "is_deletable": True,
            "can_create": True,
            "link_fields": link_fields,
        }
    )


@router.get("/{office_id}", response_class=HTMLResponse)
async def get_ukrpost_office_by_id(request: Request, office_id: int,
                                    session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    office = await crud.get_ukrpost_offices_field_data(session, office_id)
    data = office.model_dump()

    return templates.TemplateResponse(
        "pages/detail.html",
        context={
            "request": request,
            "data": data,
            "page_title": "Ukrpost Offices",
            "model_name": "Ukrpost Office"
        }
    )


@router.get("/{office_id}/edit", response_class=HTMLResponse)
async def edit_ukrpost_office_by_id(request: Request, office_id: int,
                            session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    office = await crud.get_ukrpost_offices_field_data(session, office_id)

    identifier = office.office_number

    form = UkrpostOfficeEditForm(data=office.model_dump())

    return templates.TemplateResponse(
        "pages/edit.html",
        context={
            "request": request,
            "form": form,
            "page_title": "Edit Ukrpost Office",
            "model_name": "Ukrpost Office",
            "identifier": identifier
        }
    )
