from sqlalchemy.ext.asyncio import AsyncSession

from ..book_info.crud import get_book_info_list_for_admin_page
from ..authors.crud import get_authors_list_for_admin_page
from ..book_translators.crud import get_book_translators_for_admin_page
from ..book_illustrators.crud import get_book_illustrator_for_admin_page
from ..book_series.crud import get_book_series_for_admin_page
from ..category.crud import get_categories_for_admin_page
from ..double_subcategories.crud import get_double_subcategories_for_admin_page
from ..publishing.crud import get_publishing_list_for_admin_page
from ..literatute_periods.crud import get_literature_periods_for_admin_page


class FieldsSetter:
    def __init__(self, session: AsyncSession, form):
        self.__form = form
        self.__session = session

    async def set_book_info_in_form_options(self):
        book_info_data = await get_book_info_list_for_admin_page(self.__session)
        choices = [(info.id, info.id) for info in book_info_data]
        self.__form.book_info_id.choices = choices

    async def set_authors_in_form_options(self):
        authors = await get_authors_list_for_admin_page(self.__session)
        choices = [(author.id, f"{author.first_name} {author.last_name}") for author in authors]
        self.__form.author_ids.choices = choices

    async def set_translators_in_form_options(self):
        translators = await get_book_translators_for_admin_page(self.__session)
        choices = [(t.id, f"{t.first_name} {t.last_name}") for t in translators]
        self.__form.translators_ids.choices = choices

    async def set_illustrators_in_form_options(self):
        illustrators = await get_book_illustrator_for_admin_page(self.__session)
        choices = [(i.id, f"{i.first_name} {i.last_name}") for i in illustrators]
        self.__form.illustrators_ids.choices = choices

    async def set_book_seria_in_form_options(self):
        book_series = await get_book_series_for_admin_page(self.__session)
        choices = [(0, "---")] + [(s.id, s.title) for s in book_series]
        self.__form.seria_id.choices = choices

    async def set_categories_in_form_options(self):
        categories = await get_categories_for_admin_page(self.__session)
        choices = [(cat.id, cat.title) for cat in categories]
        self.__form.categories_ids.choices = choices

    async def set_double_subcategories_in_form_options(self):
        double_subcategories = await get_double_subcategories_for_admin_page(self.__session)
        choices = [(d.id, d.title) for d in double_subcategories]
        self.__form.double_subcategories_ids.choices = choices

    async def set_publishing_in_form_options(self):
        publishing = await get_publishing_list_for_admin_page(self.__session)
        choices = [(p.id, p.title) for p in publishing]
        self.__form.publishing_id.choices = choices

    async def set_literature_periods_in_form_options(self):
        periods = await get_literature_periods_for_admin_page(self.__session)
        choices = [(0, "---")] + [(p.id, p.title) for p in periods]
        self.__form.literature_period_id.choices = choices

    async def main(self):
        for attr_name in dir(self):
            if attr_name.startswith("set_") and callable(getattr(self, attr_name)):
                await getattr(self, attr_name)()