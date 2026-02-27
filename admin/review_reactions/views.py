from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from core.models import db_helper
from .schema import ReviewReactionsForAdminList
from ..config import templates
from . import crud
from ..utils import convert_alchemy_datetime

router = APIRouter(tags=["Review Reaction for Admin Page"])


@router.get("/list", response_class=HTMLResponse)
async def get_review_reactions(request: Request, session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    review_reactions = await crud.get_review_reactions_for_admin_page(session)
    review_reactions = [reaction.model_dump() for reaction in review_reactions]

    for reaction in review_reactions:
        reaction["created_at"] = convert_alchemy_datetime(reaction["created_at"])

    fields = list(ReviewReactionsForAdminList.model_fields.keys())
    link_fields = ["user_email", "review_title"]

    return templates.TemplateResponse(
        "pages/list.html",
        context={
            "request": request,
            "data": review_reactions,
            "fields": fields,
            "is_editable": True,
            "is_deletable": True,
            "can_create": True,
            "link_fields": link_fields
        }
    )