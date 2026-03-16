from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse

from core.models import db_helper
from .forms import AuthorFactsForm, CreateAuthorFactsForm
from .schema import AuthorFactsForAdminPage, EditAuthorFact, CreateAuthorFact
from ..config import templates
from . import crud

router = APIRouter(tags=["Author Facts For Admin Page"])


@router.get("/list", name="admin_author_facts_list", response_class=HTMLResponse)
async def author_facts_list(request: Request, session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    author_facts = await crud.get_author_facts_for_admin_page(session)
    author_facts = [fact.model_dump() for fact in author_facts]

    fields = list(AuthorFactsForAdminPage.model_fields.keys())
    link_fields = ["author_name"]

    return templates.TemplateResponse(
        "pages/list.html",
        context={
            "request": request,
            "data": author_facts,
            "page_title": "Author Facts",
            "model_name": "Author Fact",
            "fields": fields,
            "is_editable": True,
            "is_deletable": True,
            "can_create": True,
            "link_fields": link_fields,
        }
    )


@router.get("/create", response_class=HTMLResponse)
async def create_author_fact_page(request: Request,
                                  session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    form = CreateAuthorFactsForm()

    await crud.set_author_in_choices(session, form)

    return templates.TemplateResponse(
        "pages/create.html",
        {
            "request": request,
            "form": form,
            "page_title": "Create Author Fact",
            "model_name": "Author Fact",
        }
    )


@router.post("/create", name="admin_create_author_fact", response_class=HTMLResponse)
async def create_author_fact_submit(request: Request,
                                    session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    form_data = await request.form()
    form = CreateAuthorFactsForm(form_data)

    await crud.set_author_in_choices(session, form)

    if form.validate():
        fact_data = CreateAuthorFact(**form_data)
        await crud.create_author_fact(session, fact_data)

        return RedirectResponse(url=request.url_for("admin_author_facts_list"), status_code=status.HTTP_303_SEE_OTHER)

    return templates.TemplateResponse(
        "pages/create.html",
        {
            "request": request,
            "form": form,
            "page_title": "Create Author Facts",
            "model_name": "Author Fact"
        }
    )


@router.get("/{fact_id}", response_class=HTMLResponse)
async def get_author_fact_by_id(request: Request, fact_id: int,
                                session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    author_fact = await crud.get_author_fact_field_data(session, fact_id)
    data = author_fact.model_dump()


    return templates.TemplateResponse(
        "pages/detail.html",
        context={
            "request": request,
            "data": data,
            "page_title": "Author Facts",
            "model_name": "Author Fact"
        }
    )


@router.get("/{fact_id}/edit", response_class=HTMLResponse)
async def edit_author_fact_by_id(request: Request, fact_id: int,
                                 session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    fact = await crud.get_author_fact_field_data(session, fact_id)

    identifier = f"{fact.author_name}"

    form = AuthorFactsForm(data=fact.model_dump())

    await crud.set_author_in_choices(session, form)

    return templates.TemplateResponse(
        "pages/edit.html",
        context={
            "request": request,
            "form": form,
            "page_title": "Edit Author Fact Text",
            "model_name": "Author Fact",
            "identifier": identifier,
        }
    )


@router.post("/{fact_id}/edit", name="admin_edit_author_fact", response_class=HTMLResponse)
async def edit_author_fact_submit(request: Request, fact_id: int,
                                  session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    form_data = await request.form()
    form = AuthorFactsForm(data=form_data)

    fact = await crud.get_author_fact_field_data(session, fact_id)
    identifier = f"{fact.author_name}"

    await crud.set_author_in_choices(session, form)

    if form.validate():
        fact_data = EditAuthorFact(**form_data)
        await crud.update_author_fact(session, fact_id, fact_data)

        return RedirectResponse(
            url=request.url_for("admin_edit_author_fact", fact_id=fact_id),
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