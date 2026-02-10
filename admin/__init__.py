from .authors_admin import AuthorsAdmin
from .banners_admin import BannerAdmin
from .cities_admin import CityAdmin
from .countries_admin import CountryAdmin
from .publishing_admin import PublishingAdmin
from .sidebar_admin import SidebarAdmin
from .users_admin import UserAdmin

admin_models = (AuthorsAdmin, UserAdmin, CountryAdmin, CityAdmin, BannerAdmin, SidebarAdmin,
                PublishingAdmin )