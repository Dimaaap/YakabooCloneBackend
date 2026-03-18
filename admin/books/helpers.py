from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Book


def to_int_list(values):
    return [int(v) for v in values] if values else None


def prepare_data_to_db(form_data):
    data = dict(form_data)

    if data.get("promo_price") == "":
        data["promo_price"] = None

    data["author_ids"] = to_int_list(form_data.getlist("author_ids"))
    data["illustrators_ids"] = to_int_list(form_data.getlist("illustrators_ids"))
    data["translators_ids"] = to_int_list(form_data.getlist("translators_ids"))
    data["categories_ids"] = to_int_list(form_data.getlist("categories_ids"))
    data["double_subcategories_ids"] = to_int_list(form_data.getlist("double_subcategories_ids"))

    data["price"] = int(data["price"])
    data["book_info_id"] = int(data["book_info_id"])

    if data["literature_period_id"] in ("0", 0, "", None):
        data["literature_period_id"] = None
    if data["seria_id"] in ("0", 0, "", None):
        data["seria_id"] = None


async def set_m2m(session: AsyncSession, book: Book, field_name: str, model, ids: list[int] | None):
    if ids:
        result = await session.execute(
            select(model).where(model.id.in_(ids))
        )
        result = result.scalars().unique().all()
        setattr(book, field_name, result)
    else:
        setattr(book, field_name, [])
        return
