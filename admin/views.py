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
from .delivery_terms import router as delivery_terms_router
from .double_subcategories import router as double_subcategories_router
from .email_subs import router as email_subs_router
from .footer import router as footer_router
from .interesting import router as interesting_router
from .knowledges import router as knowledge_router
from .literatute_periods import router as literature_periods_router
from .main_page_title import router as main_page_titles_router
from .meest_post_offices import router as meest_post_offices_router
from .new_post_offices import router as new_post_offices_router
from .new_post_postomats import router as new_post_postomats_router
from .orders import router as orders_router
from .payment_methods import router as payment_methods_router
from .promo_categories import router as promo_categories_router
from .promo_codes import router as promo_codes_router
from .promo_code_usages import router as promo_code_usages_router
from .promotions import router as promotions_router
from .publishing import router as publishing_router
from .reviews import router as reviews_router
from .review_reactions import router as review_reactions_router
from .sidebar import router as sidebar_router
from .book_info import router as book_info_router
from .books import router as books_router

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
router.include_router(delivery_terms_router)
router.include_router(double_subcategories_router)
router.include_router(email_subs_router)
router.include_router(footer_router)
router.include_router(interesting_router)
router.include_router(knowledge_router)
router.include_router(literature_periods_router)
router.include_router(main_page_titles_router)
router.include_router(meest_post_offices_router)
router.include_router(new_post_offices_router)
router.include_router(new_post_postomats_router)
router.include_router(orders_router)
router.include_router(payment_methods_router)
router.include_router(promo_categories_router)
router.include_router(promo_codes_router)
router.include_router(promo_code_usages_router)
router.include_router(promotions_router)
router.include_router(publishing_router)
router.include_router(reviews_router)
router.include_router(review_reactions_router)
router.include_router(sidebar_router)
router.include_router(book_info_router)
router.include_router(books_router)

@router.get("/", response_class=HTMLResponse)
async def index_page(request: Request):
    return templates.TemplateResponse(
        "pages/index.html",
        context={"request": request},
    )