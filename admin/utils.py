entities_slug = {
    "Users": {"image_src": "user.svg", "slug": "users"}
}


def inject_entities(request):
    return {"entities": entities_slug}
