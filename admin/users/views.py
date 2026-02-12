from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from core.models import db_helper
from ..config import templates
from . import crud

router = APIRouter(tags=["Admin Users"])


@router.get("/list", response_class=HTMLResponse)
async def users_list(request: Request, session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    users = await crud.get_users_list_for_admin_page(session)
    print(users)
    return templates.TemplateResponse(
        "pages/users/list.html",
        context={"request": request, "users": users},
    )