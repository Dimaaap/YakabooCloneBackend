import os

entities_slug = {
    "Users": {"image_src": "user.svg", "slug": "users"},
    "Countries": {"image_src": "earth.svg", "slug": "countries"},
    "Cities": {"image_src": "earth.svg", "slug": "cities"},
    "Authors": {"image_src": "author.svg", "slug": "authors"},
    "Banners": {"image_src": "banner.svg", "slug": "banners"},
    "Book Illustrators": {"image_src": "book_illustrators.svg", "slug": "book_illustrators"},
    "Book Series": {"image_src": "book_shelf.svg", "slug": "book_series"},
    "Book Translators": {"image_src": "translator.svg", "slug": "book_translators"},
    "Book Categories": {"image_src": "categories.svg", "slug": "categories"},
    "Contacts": {"image_src": "contacts.svg", "slug": "contacts"},
    "Delivery Terms": {"image_src": "delivery.svg", "slug": "delivery_terms"},
    "Book Double Subcategories": {"image_src": "categories.svg", "slug": "double_subcategories"},
    "Email Subs": {"image_src": "email.svg", "slug": "email_subs"},
    "Footers": {"image_src": "footer.svg", "slug": "footers"},
    "Interesting": {"image_src": "fire.svg", "slug": "interesting"},
    "Knowledge": {"image_src": "fire.svg", "slug": "knowledge"},
    "Literature Periods": {"image_src": "periods.svg", "slug": "literature_periods"},
    "Main Page Title": {"image_src": "title.svg", "slug": "main_page_title"},
    "Meest Post Offices": {"image_src": "meest_post.svg", "slug": "meest_post_offices"},
    "New Post Offices": {"image_src": "new_post.svg", "slug": "new_post_offices"},
    "New Post Postomats": {"image_src": "new_post.svg", "slug": "new_post_postomats"},
    "Orders": {"image_src": "order.svg", "slug": "orders"},
    "Payment Methods": {"image_src": "payment.svg", "slug": "payment_methods"},
    "Promo Categories": {"image_src": "promotions.svg", "slug": "promo_categories"},
    "Promo Codes": {"image_src": "promotions.svg", "slug": "promo_codes"},
    "Promo Code Usages": {"image_src": "promotions.svg", "slug": "promo_code_usages"},
    "Promotions": {"image_src": "promotions.svg", "slug": "promotions"},
    "Publishing": {"image_src": "publishing.svg", "slug": "publishing"},
}


def inject_entities(request):
    return {"entities": entities_slug,
            "base_url": os.getenv("ADMIN_URL")}


def convert_alchemy_datetime(datetime):
    return datetime.strftime("%Y-%m-%d")