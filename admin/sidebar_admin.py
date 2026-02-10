from sqladmin import ModelView

from core.models import Sidebar


class SidebarAdmin(ModelView, model=Sidebar):
    column_list = [Sidebar.title, Sidebar.slug, Sidebar.icon,
                   Sidebar.visible, Sidebar.order_number,
                   Sidebar.is_clickable, Sidebar.link]
    column_details_list = column_list

    column_default_sort = [
        (Sidebar.order_number, False)
    ]

    can_create = True
    can_edit = True