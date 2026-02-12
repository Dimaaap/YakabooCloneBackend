from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from .config import templates

router = APIRouter(tags=["Admin page"])


@router.get("/", response_class=HTMLResponse)
async def index_page(request: Request):
    return templates.TemplateResponse(
        "pages/index.html",
        context={"request": request}
    )