from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse

from core.models import db_helper
from entities.authors.schemas import AuthorUpdate
from .forms import AuthorEditForm
from .schema import AuthorsListForAdmin
from ..config import templates
from . import crud

router = APIRouter(tags=["Authors for Admin Page"])


@router.get("/list", response_class=HTMLResponse)
async def authors_list(request: Request, session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    authors = await crud.get_authors_list_for_admin_page(session)
    authors = [author.model_dump() for author in authors]
    fields = list(AuthorsListForAdmin.model_fields.keys())
    link_fields = ["images_src", "interesting_fact"]

    return templates.TemplateResponse(
        "pages/list.html",
        context={
            "request": request,
            "data": authors,
            "page_title": "All Authors",
            "model_name": "Author",
            "fields": fields,
            "is_editable": True,
            "is_deletable": True,
            "can_create": True,
            "link_fields": link_fields,
        }
    )


@router.get("/{author_id}", response_class=HTMLResponse)
async def get_author_by_id(request: Request, author_id: int,
                           session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    author = await crud.get_author_field_data(session, author_id)
    data = author.model_dump()

    return templates.TemplateResponse(
        "pages/detail.html",
        context={
            "request": request,
            "data": data,
            "page_title": "Authors",
            "model_name": "Author",
        }
    )


@router.get("/{author_id}/edit", response_class=HTMLResponse)
async def edit_author_by_id(request: Request, author_id: int,
                            session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    author = await crud.get_author_field_data(session, author_id)

    identifier = f"{author.first_name} {author.last_name}"

    form = AuthorEditForm(data=author.model_dump())

    return templates.TemplateResponse(
        "pages/edit.html",
        {
            "request": request,
            "form": form,
            "page_title": "Edit Author",
            "model_name": "Author",
            "identifier": identifier
        }
    )


@router.post("/{author_id}/edit", name="admin_edit_author", response_class=HTMLResponse)
async def edit_author_submit(request: Request, author_id: int,
                             session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    form_data = await request.form()
    form = AuthorEditForm(form_data)

    author = await crud.get_author_field_data(session, author_id)
    identifier = f"{author.first_name} {author.last_name}"

    if form.validate():
        author_data = AuthorUpdate(**form_data)
        await crud.update_author(session, author_id, author_data)

        return RedirectResponse(
            url=request.url_for("admin_edit_author", author_id=author_id),
            status_code=status.HTTP_303_SEE_OTHER
        )

    return templates.TemplateResponse(
        "pages/edit.html",
        {
            "request": request,
            "form": form,
            "page_title": "Edit Author",
            "model_name": "Author",
            "identifier": identifier
        }
    )