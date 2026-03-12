from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse

from core.models import db_helper
from .forms import ReviewEditForm
from .schema import ReviewsForAdminList, EditReview
from ..config import templates
from . import crud
from ..utils import convert_alchemy_datetime

router = APIRouter(tags=["Reviews For Admin Page"])


@router.get("/list", response_class=HTMLResponse)
async def get_reviews(request: Request, session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    reviews = await crud.get_reviews_list_for_admin_page(session)
    reviews = [review.model_dump() for review in reviews]

    for review in reviews:
        review["created_date"] = convert_alchemy_datetime(review["created_date"])

    fields = list(ReviewsForAdminList.model_fields.keys())
    link_fields = ["user_email", "book_title"]

    return templates.TemplateResponse(
        "pages/list.html",
        context={
            "request": request,
            "data": reviews,
            "fields": fields,
            "page_title": "Reviews",
            "model_name": "Review",
            "is_editable": True,
            "is_deletable": True,
            "can_create": True,
            "link_fields": link_fields,
        }
    )


@router.get("/{review_slug}", response_class=HTMLResponse)
async def get_review_by_id(request: Request, review_slug: str,
                           session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    review = await crud.get_reviews_field_data(session, review_slug)
    data = review.model_dump()

    return templates.TemplateResponse(
        "pages/detail.html",
        context={
            "request": request,
            "data": data,
            "page_title": "Reviews",
            "model_name": "Review"
        }
    )


@router.get("/{review_title}/edit", response_class=HTMLResponse)
async def edit_review_by_slug(request: Request, review_title: str,
                            session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    review = await crud.get_reviews_field_data(session, review_title)
    identifier = review.title or f"{review.book_title} ({review.user_email})"

    form = ReviewEditForm(data=review.model_dump())

    return templates.TemplateResponse(
        "pages/edit.html",
        context={
            "request": request,
            "form": form,
            "page_title": "Edit Review",
            "model_name": "Review",
            "identifier": identifier
        }
    )


@router.post("/{review_title}/edit", name="admin_edit_review", response_class=HTMLResponse)
async def edit_review_submit(request: Request, review_title: str,
                                session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    form_data = await request.form()
    form = ReviewEditForm(formdata=form_data)

    review = await crud.get_reviews_field_data(session, review_title)
    identifier = review.title or f"{review.book_title} ({review.user_email})"


    if form.validate():
        review_data = EditReview(**form.data)
        await crud.update_review(session, review_title, review_data)

        return RedirectResponse(
            url=request.url_for("admin_edit_review", review_title=review_title),
            status_code=status.HTTP_303_SEE_OTHER
        )

    return templates.TemplateResponse(
        "pages/edit.html",
        {
            "request": request,
            "form": form,
            "page_title": "Edit Review",
            "model_name": "Review",
            "identifier": identifier
        }
    )
