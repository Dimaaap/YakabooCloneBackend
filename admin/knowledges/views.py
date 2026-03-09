from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from core.models import db_helper
from .forms import KnowledgeEditForm
from .schema import KnowledgeForAdminPageList
from ..config import templates
from . import crud

router = APIRouter(tags=["Admin Knowledge"])


@router.get("/list", response_class=HTMLResponse)
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
