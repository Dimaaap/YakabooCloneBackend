from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse

from core.models import db_helper
from .forms import KnowledgeEditForm, KnowledgeCreateForm
from .schema import KnowledgeForAdminPageList, EditKnowledge, CreateKnowledge
from ..config import templates
from . import crud

router = APIRouter(tags=["Admin Knowledge"])


@router.get("/list", name="admin_knowledge_list", response_class=HTMLResponse)
async def knowledge_list(request: Request, session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    all_knowledge = await crud.get_knowledge_list_for_admin_page(session)
    all_knowledge = [knowledge.model_dump() for knowledge in all_knowledge]

    fields = list(KnowledgeForAdminPageList.model_fields.keys())

    return templates.TemplateResponse(
        "pages/list.html",
        context={
            "request": request,
            "data": all_knowledge,
            "page_title": "All knowledge",
            "model_name": "Knowledge",
            "fields": fields,
            "is_editable": True,
            "is_deletable": True,
            "can_create": True,
        }
    )


@router.get("/create", response_class=HTMLResponse)
async def create_knowledge_page(request: Request):
    form = KnowledgeCreateForm()

    return templates.TemplateResponse(
        "pages/create.html",
        {
            "request": request,
            "form": form,
            "page_title": "Create knowledge",
            "model_name": "Knowledge"
        }
    )


@router.post("/create", name="admin_create_knowledge", response_class=HTMLResponse)
async def create_knowledge_submit(request: Request,
                                  session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    form_data = await request.form()
    form = KnowledgeCreateForm(form_data)

    if form.validate():
        knowledge_data = CreateKnowledge(**form.data)
        await crud.create_knowledge(session, knowledge_data)

        return RedirectResponse(
            url=request.url_for("admin_knowledge_list"),
            status_code=status.HTTP_303_SEE_OTHER
        )

    return templates.TemplateResponse(
        "pages/create.html",
        {
            "request": request,
            "form": form,
            "page_title": "Create knowledge",
            "model_name": "Knowledge"
        }
    )


@router.get("/{knowledge_slug}", response_class=HTMLResponse)
async def get_knowledge_by_id(request: Request, knowledge_slug: str,
                              session: AsyncSession=Depends(db_helper.scoped_session_dependency)):

    knowledge = await crud.get_knowledge_field_data(session, knowledge_slug)
    data = knowledge.model_dump()

    return templates.TemplateResponse(
        "pages/detail.html",
        context={
            "request": request,
            "data": data,
            "page_title": "Knowledge",
            "model_name": "Knowledge"
        }
    )


@router.get("/{knowledge_slug}/edit", response_class=HTMLResponse)
async def edit_interesting_by_id(request: Request, knowledge_slug: str,
                            session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    knowledge = await crud.get_knowledge_field_data(session, knowledge_slug)

    identifier = knowledge.title

    form = KnowledgeEditForm(data=knowledge.model_dump())

    return templates.TemplateResponse(
        "pages/edit.html",
        context={
            "request": request,
            "form": form,
            "page_title": "Edit Knowledge",
            "model_name": "Knowledge",
            "identifier": identifier
        }
    )


@router.post("/{knowledge_slug}/edit", name="admin_edit_knowledge", response_class=HTMLResponse)
async def edit_knowledge_submit(request: Request, knowledge_slug: str,
                                session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    form_data = await request.form()
    form = KnowledgeEditForm(data=form_data)

    knowledge = await crud.get_knowledge_field_data(session, knowledge_slug)
    identifier = knowledge.title

    if form.validate():
        knowledge_data = EditKnowledge(**form.data)
        await crud.update_knowledge(session, knowledge_slug, knowledge_data)

        return RedirectResponse(
            url=request.url_for("admin_edit_knowledge", knowledge_slug=knowledge_slug),
            status_code=status.HTTP_303_SEE_OTHER
        )

    return templates.TemplateResponse(
        "pages/edit.html",
        {
            "request": request,
            "form": form,
            "page_title": "Edit Knowledge",
            "model_name": "Knowledge",
            "identifier": identifier
        }
    )