from sqladmin import ModelView

from core.models import City


class CityAdmin(ModelView, model=City):

    column_list = [City.title, City.is_visible, City.region,
                   City.country]
    column_details_list = column_list
    column_default_sort = [
        (City.title, False)
    ]

    column_formatters = {
        City.country: lambda x, y: x.country,
    }

    can_create = True
    can_edit = True
    name = "Cities"
    name_plural = name