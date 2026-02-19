from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from .config import templates
from .users import router as users_router
from .countries import router as countries_router
from .cities import router as cities_router
from .authors import router as authors_router
from .banners import router as banners_router
from .book_illustrators import router as book_illustrators_router
from .book_series import router as book_series_router
from .book_translators import router as book_translators_router
from .category import router as category_router
from .contacts import router as contacts_router

router = APIRouter(tags=["Admin page"])
router.include_router(users_router)
router.include_router(countries_router)
router.include_router(cities_router)
router.include_router(authors_router)
router.include_router(banners_router)
router.include_router(book_illustrators_router)
router.include_router(book_series_router)
router.include_router(book_translators_router)
router.include_router(category_router)
router.include_router(contacts_router)


@router.get("/", response_class=HTMLResponse)
async def index_page(request: Request):
    return templates.TemplateResponse(
        "pages/index.html",
        context={"request": request},
    )