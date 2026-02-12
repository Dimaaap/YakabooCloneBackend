from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from .config import templates
from .users import router as users_router

router = APIRouter(tags=["Admin page"])
router.include_router(users_router)


@router.get("/", response_class=HTMLResponse)
async def index_page(request: Request):
    return templates.TemplateResponse(
        "pages/index.html",
        context={"request": request},
    )