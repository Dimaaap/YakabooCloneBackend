from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from .config import templates
from .users import router as users_router
from .countries import router as countries_router
from .cities import router as cities_router
from .authors import router as authors_router
from .banners import router as banners_router

router = APIRouter(tags=["Admin page"])
router.include_router(users_router)
router.include_router(countries_router)
router.include_router(cities_router)
router.include_router(authors_router)
router.include_router(banners_router)


@router.get("/", response_class=HTMLResponse)
async def index_page(request: Request):
    return templates.TemplateResponse(
        "pages/index.html",
        context={"request": request},
    )