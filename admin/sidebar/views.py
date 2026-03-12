from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse

from core.models import db_helper
from .forms import SidebarsEditForm
from .schema import SidebarsForAdminPage, EditSidebar
from ..config import templates
from . import crud

router = APIRouter(tags=["Sidebars For Admin Page"])


@router.get("/list", response_class=HTMLResponse)
async def get_sidebars(request: Request, session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    sidebars = await crud.get_sidebars_list_for_admin_page(session)
    sidebars = [sidebar.model_dump() for sidebar in sidebars]

    fields = list(SidebarsForAdminPage.model_fields.keys())

    return templates.TemplateResponse(
        "pages/list.html",
        context={
            "request": request,
            "data": sidebars,
            "fields": fields,
            "page_title": "Sidebars",
            "model_name": "Sidebar",
            "is_editable": True,
            "is_deletable": True,
            "can_create": True
        }
    )


@router.get("/{sidebar_id}", response_class=HTMLResponse)
async def get_sidebar_by_id(request: Request, sidebar_id: int,
                           session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    review = await crud.get_sidebars_field_data(session, sidebar_id)
    data = review.model_dump()

    return templates.TemplateResponse(
        "pages/detail.html",
        context={
            "request": request,
            "data": data,
            "page_title": "Sidebars",
            "model_name": "Sidebar",
        }
    )


@router.get("/{sidebar_id}/edit", response_class=HTMLResponse)
async def edit_sidebar_by_id(request: Request, sidebar_id: int,
                            session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    sidebar = await crud.get_sidebars_field_data(session, sidebar_id)
    identifier = sidebar.title

    form = SidebarsEditForm(data=sidebar.model_dump())

    return templates.TemplateResponse(
        "pages/edit.html",
        context={
            "request": request,
            "form": form,
            "page_title": "Edit Sidebar",
            "model_name": "Sidebar",
            "identifier": identifier
        }
    )


@router.post("/{sidebar_id}/edit", name="admin_edit_sidebar", response_class=HTMLResponse)
async def edit_sidebar_submit(request: Request, sidebar_id: int,
                                session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    form_data = await request.form()
    form = SidebarsEditForm(formdata=form_data)

    sidebar = await crud.get_sidebars_field_data(session, sidebar_id)
    identifier = sidebar.title


    if form.validate():
        sidebar_data = EditSidebar(**form.data)
        await crud.update_sidebar(session, sidebar_id, sidebar_data)

        return RedirectResponse(
            url=request.url_for("admin_edit_sidebar", sidebar_id=sidebar_id),
            status_code=status.HTTP_303_SEE_OTHER
        )

    return templates.TemplateResponse(
        "pages/edit.html",
        {
            "request": request,
            "form": form,
            "page_title": "Edit Sidebar",
            "model_name": "Sidebar",
            "identifier": identifier
        }
    )
