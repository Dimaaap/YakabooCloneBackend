
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse

from core.models import db_helper
from .forms import UserEditForm
from .schema import UserListForAdmin, UserUpdate
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


@router.get("/{user_id}/edit", response_class=HTMLResponse)
async def edit_user_by_id(request: Request, user_id: int,
                          session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    user = await crud.get_user_field_data(session, user_id)

    identifier = f"{user.first_name} {user.last_name}"

    form = UserEditForm(data=user.model_dump())

    return templates.TemplateResponse(
        "pages/edit.html",
        context={
            "request": request,
            "form": form,
            "page_title": "Edit User",
            "model_name": "User",
            "identifier": identifier
        }
    )


@router.post("/{user_id}/edit", name="admin_edit_user", response_class=HTMLResponse)
async def edit_user_submit(request: Request, user_id: int,
                           session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    form_data = await request.form()
    form = UserEditForm(form_data)

    user = await crud.get_user_field_data(session, user_id)
    identifier = f"{user.first_name} {user.last_name}"

    if form.validate():
        user_data = UserUpdate(**form.data)
        await crud.update_user(session, user_id, user_data)

        return RedirectResponse(
            url=request.url_for("admin_edit_user", user_id=user_id),
            status_code=status.HTTP_303_SEE_OTHER
        )

    return templates.TemplateResponse(
        "pages/edit.html",
        context={
            "request": request,
            "form": form,
            "page_title": "Edit User",
            "identifier": identifier
        }
    )