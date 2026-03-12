from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse

from core.models import db_helper
from .forms import ReviewReactionsEditForm
from .schema import ReviewReactionsForAdminList, EditReviewReaction
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


@router.get("/{reaction_id}", response_class=HTMLResponse)
async def get_review_reaction_by_id(request: Request, reaction_id: int,
                                    session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    reaction = await crud.get_review_reactions_field_data(session, reaction_id)
    data = reaction.model_dump()

    return templates.TemplateResponse(
        "pages/detail.html",
        context={
            "request": request,
            "data": data,
            "page_title": "Review Reactions",
            "model_name": "Review Reaction"
        }
    )


@router.get("/{reaction_id}/edit", response_class=HTMLResponse)
async def edit_review_reaction_by_id(request: Request, reaction_id: int,
                            session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    review_reaction = await crud.get_review_reactions_field_data(session, reaction_id)
    identifier = f"{review_reaction.review_title} {review_reaction.user_email}"

    form = ReviewReactionsEditForm(data=review_reaction.model_dump())

    return templates.TemplateResponse(
        "pages/edit.html",
        context={
            "request": request,
            "form": form,
            "page_title": "Edit Review Reaction",
            "model_name": "Review Reaction",
            "identifier": identifier
        }
    )


@router.post("/{reaction_id}/edit", name="admin_edit_review_reaction", response_class=HTMLResponse)
async def edit_review_reaction_submit(request: Request, reaction_id: int,
                                session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    form_data = await request.form()
    form = ReviewReactionsEditForm(formdata=form_data)

    reaction = await crud.get_review_reactions_field_data(session, reaction_id)
    identifier = f"{reaction.review_title} {reaction.user_email}"

    if form.validate():
        reaction_data = EditReviewReaction(**form.data)
        await crud.update_review_reaction(session, reaction_id, reaction_data)

        return RedirectResponse(
            url=request.url_for("admin_edit_review_reaction", reaction_id=reaction_id),
            status_code=status.HTTP_303_SEE_OTHER
        )

    return templates.TemplateResponse(
        "pages/edit.html",
        {
            "request": request,
            "form": form,
            "page_title": "Edit Review Reaction",
            "model_name": "Review Reaction",
            "identifier": identifier
        }
    )
