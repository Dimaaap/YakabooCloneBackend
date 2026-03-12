from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse

from core.models import db_helper
from .forms import MainPageTitleEditForm
from .schema import MainPageTitlesListForAdmin, EditMainPageTitle
from ..config import templates
from . import crud
from ..utils import convert_alchemy_datetime

router = APIRouter(tags=["Main Page Titles for Admin"])


@router.get("/list", response_class=HTMLResponse)
async def get_main_page_titles(request: Request, session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    main_page_titles = await crud.get_main_page_titles_for_admin_page(session)
    main_page_titles = [title.model_dump() for title in main_page_titles]

    for title in main_page_titles:
        title["created_at"] = convert_alchemy_datetime(title["created_at"])
        title["updated_at"] = convert_alchemy_datetime(title["updated_at"])

    fields = list(MainPageTitlesListForAdmin.model_fields.keys())

    return templates.TemplateResponse(
        "pages/list.html",
        context={
            "request": request,
            "data": main_page_titles,
            "page_title": "All Main Page Titles",
            "model_name": "Main Page Title",
            "fields": fields,
            "is_editable": True,
            "is_deletable": True,
            "can_create": True,
        }
    )


@router.get("/{title_id}", response_class=HTMLResponse)
async def get_main_page_title_by_id(request: Request, title_id: int,
                                    session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    main_page_title = await crud.get_main_page_title_field_data(session, title_id)
    data = main_page_title.model_dump()

    return templates.TemplateResponse(
        "pages/detail.html",
        context={
            "request": request,
            "data": data,
            "page_title": "Main Page Titles",
            "model_name": "Main Page Title"
        }
    )


@router.get("/{title_id}/edit", response_class=HTMLResponse)
async def edit_interesting_by_id(request: Request, title_id: int,
                            session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    title = await crud.get_main_page_title_field_data(session, title_id)

    identifier = title.title

    form = MainPageTitleEditForm(data=title.model_dump())

    return templates.TemplateResponse(
        "pages/edit.html",
        context={
            "request": request,
            "form": form,
            "page_title": "Edit Main Page Title",
            "model_name": "Main Pate Title",
            "identifier": identifier
        }
    )


@router.post("/{title_id}/edit", name="admin_edit_main_page_title", response_class=HTMLResponse)
async def edit_main_page_title_submit(request: Request, title_id: int,
                                session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    form_data = await request.form()
    form = MainPageTitleEditForm(data=form_data)

    title = await crud.get_main_page_title_field_data(session, title_id)
    identifier = title.title

    if form.validate():
        main_page_title_data = EditMainPageTitle(**form.data)
        await crud.update_main_page_title(session, title_id, main_page_title_data)

        return RedirectResponse(
            url=request.url_for("admin_edit_main_page_title", title_id=title_id),
            status_code=status.HTTP_303_SEE_OTHER
        )

    return templates.TemplateResponse(
        "pages/edit.html",
        {
            "request": request,
            "form": form,
            "page_title": "Edit Main Page Title",
            "model_name": "Main Pate Title",
            "identifier": identifier
        }
    )