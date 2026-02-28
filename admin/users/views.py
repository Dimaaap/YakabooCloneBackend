
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from core.models import db_helper
from .schema import UserListForAdmin
from ..config import templates
from . import crud
from ..utils import convert_alchemy_datetime

router = APIRouter(tags=["Admin Users"])


@router.get("/list", response_class=HTMLResponse)
async def users_list(request: Request, session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    users = await crud.get_users_list_for_admin_page(session)
    users = [user.model_dump() for user in users]

    for user in users:
        user["date_joined"] = convert_alchemy_datetime(user["date_joined"])
    fields = list(UserListForAdmin.model_fields.keys())

    return templates.TemplateResponse(
        "pages/list.html",
        context={
            "request": request,
            "data": users,
            "page_title": "All users",
            "model_name": "User",
            "fields": fields,
            "is_editable": True,
            "is_deletable": True,
            "can_create": True
            },
    )


@router.get("/{user_id}", response_class=HTMLResponse)
async def get_user_by_id(request: Request, user_id: int,
                         session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    user = await crud.get_user_field_data(session, user_id)
    data = user.model_dump()

    return templates.TemplateResponse(
        "pages/detail.html",
        context={
            "request": request,
            "data": data,
            "page_title": "Users",
            "model_name": "User",
        }
    )