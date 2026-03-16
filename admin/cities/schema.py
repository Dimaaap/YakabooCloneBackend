from pydantic import BaseModel, ConfigDict


class CitiesList(BaseModel):
    title: str
    is_visible: bool = True
    region: str
    country_title: str


class CitiesListForAdmin(CitiesList):
    model_config = ConfigDict(from_attributes=True)

    country_id: int
    id: int


class CitiesListAdminWithSlug(CitiesListForAdmin):
    country_slug: str


class EditCity(BaseModel):
    title: str | None = None
    is_visible: bool | None = None
    region: str | None = None
    country_id: int | None = None


class CreateCity(BaseModel):
    title: str
    is_visible: bool = True
    region: str | None = None
    country_id: int
