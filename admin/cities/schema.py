from pydantic import BaseModel, ConfigDict


class CitiesList(BaseModel):
    title: str
    is_visible: bool = True
    region: str
    country_title: str


class CitiesListForAdmin(CitiesList):
    model_config = ConfigDict(from_attributes=True)

    id: int


class CitiesListAdminWithSlug(CitiesListForAdmin):

    country_slug: int