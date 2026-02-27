from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from core.models import db_helper
from .schema import ReviewsForAdminList
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