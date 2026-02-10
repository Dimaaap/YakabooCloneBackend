from sqladmin import ModelView

from admin.formatters.main import short_text_formatter
from core.models import Author


class AuthorsAdmin(ModelView, model=Author):
    column_list = [Author.first_name, Author.last_name,
                   Author.slug, Author.date_of_birth,
                   Author.description,
                   Author.is_active, Author.short_description,
                   Author.interesting_fact]

    column_details_list = column_list
    column_searchable_list = [Author.first_name, Author.last_name]

    column_default_sort = [
        (Author.first_name, False),
        (Author.last_name, False),
    ]

    column_formatters = {
        Author.first_name: lambda m, a: f"{m.first_name}",
        Author.last_name: lambda m, a: f"{m.last_name}",
        Author.description: short_text_formatter(50),
        Author.short_description: short_text_formatter(30),
    }

    can_create = True
    can_edit = True