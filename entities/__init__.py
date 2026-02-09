from fastapi import APIRouter

from .banners import router as banners_router
from .sidebar import router as sidebars_router
from .email_subs import router as subs_router
from .knowledges import router as knowledge_router
from .users import router as auth_router
from .wishlists import router as wishlist_router
from .authors import router as authors_router
from .categories import router as categories_router
from .promotion_categories import router as promo_categories_router
from .promotions import router as promo_router
from .publishing import router as publishing_router
from .interesting import router as interesting_router
from .footers import router as footer_router
from .game_series import router as game_series_router
from .game_brands import router as game_brands_router
from .game_ages import router as game_ages_router
from .contacts import router as contacts_router
from .cities import router as cities_router
from .countries import router as countries_router
from .delivery_terms import router as delivery_terms_router
from .author_facts import router as author_facts_router
from .books import router as books_router
from .book_translators import router as book_translators_router
from .book_series import router as book_series_router
from .literature_periods import router as literature_periods_router
from .hobby_categories import router as hobby_categories_router
from .hobby_brand import router as hobby_brand_router
from .hobbies import router as hobbies_router
from .gift_brands import router as gift_brands_router
from .gift_subcategories import router as gift_subcategories_router
from .notebook_categories import router as notebook_categories_router
from .hobby_subcategories import router as hobby_subcategories_router
from .accesories import router as accessories_router
from .gift_categories import router as gift_categories_router
from .gift_subcategories import router as gift_series_router
from .gifts import router as gifts_router
from .accessories_brands import router as accessories_brands_router
from .accessories_categories import router as accessories_categories_router
from .notebook_subcategories import router as notebook_subcategories_router
from .main_page_title import router as main_page_title_router
from .book_illustrators import router as book_illustrators_router
from .book_subcategories import router as book_subcategories_router
from .book_subcategory_banners import router as book_subcategory_banners_router
from .double_subcategories import router as double_subcategories_router
from .cart_item import router as cart_item_router
from .cart import router as cart_router
from .payment_methods import router as payments_router
from .promo_codes import router as promo_codes_router
from .promo_code_usage import router as promo_code_usage_router
from .ukrpost_offices import router as ukrpost_offices_router
from .meest_post_offices import router as meest_post_offices
from .new_post_postomats import router as new_post_postomats_router
from .new_post_offices import router as new_post_offices_router
from .reviews import router as reviews_router
from .user_seen_books import router as user_seen_books_router
from .review_reactions import router as review_reactions_router
from .search import router as search_router
from .books_text import router as books_text_router
from .user_history import router as user_history_router

router = APIRouter()

router.include_router(banners_router)
router.include_router(sidebars_router)
router.include_router(subs_router)
router.include_router(knowledge_router)
router.include_router(auth_router)
router.include_router(wishlist_router)
router.include_router(authors_router)
router.include_router(categories_router)
router.include_router(promo_categories_router)
router.include_router(promo_router)
router.include_router(publishing_router)
router.include_router(interesting_router)
router.include_router(footer_router)
router.include_router(game_series_router)
router.include_router(game_brands_router)
router.include_router(game_ages_router)
router.include_router(contacts_router)
router.include_router(cities_router)
router.include_router(countries_router)
router.include_router(delivery_terms_router)
router.include_router(author_facts_router)
router.include_router(books_router)
router.include_router(book_series_router)
router.include_router(book_illustrators_router)
router.include_router(book_translators_router)
router.include_router(literature_periods_router)
router.include_router(hobby_categories_router)
router.include_router(hobby_brand_router)
router.include_router(hobbies_router)
router.include_router(hobby_subcategories_router)
router.include_router(accessories_router)
router.include_router(accessories_brands_router)
router.include_router(accessories_categories_router)
router.include_router(notebook_categories_router)
router.include_router(notebook_subcategories_router)
router.include_router(gifts_router)
router.include_router(gift_brands_router)
router.include_router(gift_subcategories_router)
router.include_router(gift_categories_router)
router.include_router(gift_series_router)
router.include_router(main_page_title_router)
router.include_router(book_subcategories_router)
router.include_router(book_subcategory_banners_router)
router.include_router(double_subcategories_router)
router.include_router(cart_item_router)
router.include_router(cart_router)
router.include_router(payments_router)
router.include_router(promo_codes_router)
router.include_router(promo_code_usage_router)
router.include_router(ukrpost_offices_router)
router.include_router(meest_post_offices)
router.include_router(new_post_postomats_router)
router.include_router(new_post_offices_router)
router.include_router(reviews_router)
router.include_router(user_seen_books_router)
router.include_router(review_reactions_router)
router.include_router(search_router)
router.include_router(books_text_router)
router.include_router(user_history_router)