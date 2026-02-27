from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from core.models import db_helper
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