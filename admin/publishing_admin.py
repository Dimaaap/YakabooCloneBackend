from sqladmin import ModelView

from admin.formatters.main import short_text_formatter
from core.models import Publishing


class PublishingAdmin(ModelView, model=Publishing):
    column_list = [Publishing.title, Publishing.slug, Publishing.logo,
                   Publishing.short_description, Publishing.long_description,
                   Publishing.visible]

    column_details_list = column_list
    column_default_sort = [
        (Publishing.title, False)
    ]

    column_formatters = {
        Publishing.long_description: short_text_formatter(50),
        Publishing.short_description: short_text_formatter(30),
    }

    can_create = True
    can_edit = True