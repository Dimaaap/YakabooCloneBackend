from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse

from core.models import db_helper
from .forms import NewPostPostomatEditForm, NewPostPostomatCreateForm
from .schema import NewPostPostomatsForAdmin, EditNewPostPostomat, CreateNewPostPostomat
from ..config import templates
from . import crud

router = APIRouter(tags=["New Post Postomats for Admin Page"])


@router.get("/list", name="admin_new_post_postomats_list", response_class=HTMLResponse)
async def get_new_post_offices(request: Request, session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    new_post_postomats = await crud.get_new_post_postomats_for_admin_page(session)
    new_post_postomats = [postomat.model_dump() for postomat in new_post_postomats]

    fields = list(NewPostPostomatsForAdmin.model_fields.keys())
    link_fields = ["city_title"]

    return templates.TemplateResponse(
        "pages/list.html",
        context={
            "request": request,
            "data": new_post_postomats,
            "page_title": "New Post Postomats",
            "model_name": "New Post Postomat",
            "fields": fields,
            "is_editable": True,
            "is_deletable": True,
            "can_create": True,
            "link_fields": link_fields,
        }
    )


@router.get("/create", response_class=HTMLResponse)
async def create_new_post_postomat_page(request: Request,
                                        session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    form = NewPostPostomatCreateForm()

    await crud.set_cities_in_choices(session, form)

    return templates.TemplateResponse(
        "pages/create.html",
        {
            "request": request,
            "form": form,
            "page_title": "Create New Post Postomat",
            "model_name": "New Post Postomat"
        }
    )


@router.post("/create", response_class=HTMLResponse)
async def create_new_post_postomat_submit(request: Request,
                                          session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    form_data = await request.form()
    form = NewPostPostomatCreateForm(form_data)

    await crud.set_cities_in_choices(session, form)

    if form.validate():
        postomat_data = CreateNewPostPostomat(**form.data)
        _ = await crud.create_new_post_postomat(session, postomat_data)

        return RedirectResponse(
            url=request.url_for("admin_new_post_postomats_list"),
            status_code=status.HTTP_303_SEE_OTHER
        )

    return templates.TemplateResponse(
        "pages/create.html",
        {
            "request": request,
            "form": form,
            "page_title": "Create New Post Postomat",
            "model_name": "New Post Postomat"
        }
    )


@router.get("/{postomat_id}", response_class=HTMLResponse)
async def get_new_post_postomat_by_id(request: Request, postomat_id: int,
                                      session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    postomat = await crud.get_new_post_postomat_field_data(session, postomat_id)
    data = postomat.model_dump()

    return templates.TemplateResponse(
        "pages/detail.html",
        context={
            "request": request,
            "data": data,
            "page_title": "New Post Postomats",
            "model_name": "New Post Postomat"
        }
    )


@router.get("/{postomat_id}/edit", response_class=HTMLResponse)
async def edit_postomat_by_id(request: Request, postomat_id: int,
                            session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    postomat = await crud.get_new_post_postomat_field_data(session, postomat_id)

    identifier = postomat.number

    form = NewPostPostomatEditForm(data=postomat.model_dump())

    return templates.TemplateResponse(
        "pages/edit.html",
        context={
            "request": request,
            "form": form,
            "page_title": "Edit New Post Postomat",
            "model_name": "New Post Postomat",
            "identifier": identifier
        }
    )


@router.post("/{postomat_id}/edit", name="admin_edit_new_post_postomat", response_class=HTMLResponse)
async def edit_new_post_postomat_submit(request: Request, postomat_id: int,
                                session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    form_data = await request.form()
    form = NewPostPostomatEditForm(data=form_data)

    postomat = await crud.get_new_post_postomat_field_data(session, postomat_id)
    identifier = postomat.number

    if form.validate():
        office_data = EditNewPostPostomat(**form.data)
        await crud.update_new_post_postomat(session, postomat_id, office_data)

        return RedirectResponse(
            url=request.url_for("admin_edit_new_post_postomat", postomat_id=postomat_id),
            status_code=status.HTTP_303_SEE_OTHER
        )

    return templates.TemplateResponse(
        "pages/edit.html",
        {
            "request": request,
            "form": form,
            "page_title": "Edit New Post Postomat",
            "model_name": "New Post Postomat",
            "identifier": identifier
        }
    )
