from sqladmin import ModelView

from core.models import User


class UserAdmin(ModelView, model=User):
    column_exclude_list = (User.password, User.seen_books, User.user_seen_books, User.reviews,
                           User.wishlists, User.cart, User.promo_usage, User.search_terms,
                           User.review_reactions)

    column_details_list = [
        User.first_name,
        User.last_name,
        User.phone_number,
        User.email,
        User.is_staff,
        User.is_verified,
        User.is_subscribed_to_news,
        User.birth_date,
        User.bonuses,
        User.level,
        User.date_joined,
    ]

    column_default_sort = [
        (User.date_joined, False)
    ]

    column_formatters = {
        User.first_name: lambda m, a: f"{m.first_name}",
        User.last_name: lambda m, a: f"{m.last_name}",
    }

    can_create = True
    can_edit = True