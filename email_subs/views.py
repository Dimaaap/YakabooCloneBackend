from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from .schemas import EmailSubSchema, EmailSubCreate, CheckEmail
from core.models import db_helper
from . import crud

router = APIRouter(tags=["Email subs"])


@router.get("/all", response_model=list[EmailSubSchema])
async def get_all_email_subs(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await crud.get_all_subs(session)


@router.post("/create", response_model=EmailSubSchema)
async def create_email_sub(request: EmailSubCreate,
                           session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await crud.create_email_sub(session=session, email=request.email)


@router.delete("/{email}")
async def delete_email_sub(
        email: str, session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.delete_sub_by_email(session=session, email=email)


@router.get("/{email}", response_model=EmailSubSchema)
async def get_sub_by_email(
        email: str,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.get_sub_by_email(session=session, email=email)
