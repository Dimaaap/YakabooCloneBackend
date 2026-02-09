from sqladmin import ModelView

from core.models import Author


class AuthorsAdmin(ModelView, model=Author):
    column_list = [Author.first_name, Author.last_name,
                   Author.slug, Author.date_of_birth,
                   Author.description,
                   Author.is_active, Author.short_description]