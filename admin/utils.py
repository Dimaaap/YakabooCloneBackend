import os

entities_slug = {
    "Users": {"image_src": "user.svg", "slug": "users"},
    "Countries": {"image_src": "earth.svg", "slug": "countries"},
    "Cities": {"image_src": "earth.svg", "slug": "cities"},
    "Authors": {"image_src": "author.svg", "slug": "authors"},
    "Banners": {"image_src": "banner.svg", "slug": "banners"},
}


def inject_entities(request):
    return {"entities": entities_slug,
            "base_url": os.getenv("ADMIN_URL")}


def convert_alchemy_datetime(datetime):
    return datetime.strftime("%Y-%m-%d")