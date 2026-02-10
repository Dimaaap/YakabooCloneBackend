from sqladmin import ModelView

from core.models import Banner


class BannerAdmin(ModelView, model=Banner):
    column_list = [Banner.image_src, Banner.visible, Banner.link, Banner.in_all_books_page]
    column_details_list = column_list

    can_create = True
    can_edit = True