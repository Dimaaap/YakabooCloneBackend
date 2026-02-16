from pydantic import BaseModel, ConfigDict


class CitiesList(BaseModel):
    title: str
    is_visible: str
    region: str
    country_title: str


class CitiesListForAdmin(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int