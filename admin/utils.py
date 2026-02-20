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
}


def inject_entities(request):
    return {"entities": entities_slug,
            "base_url": os.getenv("ADMIN_URL")}


def convert_alchemy_datetime(datetime):
    return datetime.strftime("%Y-%m-%d")