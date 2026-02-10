from sqladmin import ModelView

from core.models import Country


class CountryAdmin(ModelView, model=Country):
    column_list = [Country.title, Country.is_visible, Country.cities,
                   Country.delivery_terms]

    column_details_list = column_list
    column_default_sort = [
        (Country.title, False)
    ]

    column_formatters = {
        Country.cities: lambda x, y: [city.title for city in x.cities]
    }

    can_create = True
    can_edit = True
    name = "Countries"
    name_plural = name