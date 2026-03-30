from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse

from core.models import db_helper
from .forms import InterestingEditForm, InterestingCreateForm
from .schema import InterestingForAdminList, EditInteresting, CreateInteresting
from ..config import templates
from . import crud

router = APIRouter(tags=["Admin Interesting"])


@router.get("/list", name="admin_interesting_list", response_class=HTMLResponse)
async def interesting_list(request: Request, session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    all_interesting = await crud.get_interesting_list_for_admin_page(session)
    all_interesting = [interesting.model_dump() for interesting in all_interesting]

    fields = list(InterestingForAdminList.model_fields.keys())

    return templates.TemplateResponse(
        "pages/list.html",
        context={
            "request": request,
            "data": all_interesting,
            "page_title": "All interesting",
            "model_name": "Interesting",
            "fields": fields,
            "is_editable": True,
            "is_deletable": True,
            "can_create": True,
        }
    )


@router.get("/create", response_class=HTMLResponse)
async def create_interesting_page(request: Request):
    form = InterestingCreateForm()

    return templates.TemplateResponse(
        "pages/create.html",
        {
            "request": request,
            "form": form,
            "page_title": "Create Interesting",
            "model_name": "Interesting",
        }
    )


@router.post("/create", name="admin_create_interesting", response_class=HTMLResponse)
async def create_interesting_submit(request: Request,
                                    session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    form_data = await request.form()
    form = InterestingCreateForm(form_data)

    if form.validate():
        interesting_data = CreateInteresting(**form.data)
        await crud.create_interesting(session, interesting_data)

        return RedirectResponse(
            url=request.url_for("admin_interesting_list"),
            status_code=status.HTTP_303_SEE_OTHER
        )

    return templates.TemplateResponse(
        "pages/create.html",
        {
            "request": request,
            "form": form,
            "page_title": "Create Interesting",
            "model_name": "Interesting",
        }
    )


@router.get("/{interesting_id}", response_class=HTMLResponse)
async def get_interesting(request: Request, interesting_id: int,
                          session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    interesting = await crud.get_interesting_field_data(session, interesting_id)
    data = interesting.model_dump()

    return templates.TemplateResponse(
        "pages/detail.html",
        context={
            "request": request,
            "data": data,
            "page_title": "Interesting",
            "model_name": "Interesting"
        }
    )



@router.get("/{interesting_id}/edit", response_class=HTMLResponse)
async def edit_interesting_by_id(request: Request, interesting_id: int,
                            session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    interesting = await crud.get_interesting_field_data(session, interesting_id)

    identifier = interesting.title

    form = InterestingEditForm(data=interesting.model_dump())

    return templates.TemplateResponse(
        "pages/edit.html",
        context={
            "request": request,
            "form": form,
            "page_title": "Edit Interesting",
            "model_name": "Interesting",
            "identifier": identifier
        }
    )


@router.post("/{interesting_id}/edit", name="admin_edit_interesting", response_class=HTMLResponse)
async def edit_interesting_submit(request: Request, interesting_id: int,
                                  session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    form_data = await request.form()
    form = InterestingEditForm(data=form_data)

    interesting = await crud.get_interesting_field_data(session, interesting_id)
    identifier = interesting.title

    if form.validate():
        interesting_data = EditInteresting(**form.data)
        await crud.update_interesting(session, interesting_id, interesting_data)

        return RedirectResponse(
            url=request.url_for("admin_edit_interesting", interesting_id=interesting_id),
            status_code=status.HTTP_303_SEE_OTHER
        )

    return templates.TemplateResponse(
        "pages/edit.html",
        {
            "request": request,
            "form": form,
            "page_title": "Edit Interesting",
            "model_name": "Interesting",
            "identifier": identifier
        }
    )