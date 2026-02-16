from pydantic import BaseModel, ConfigDict


class CountriesList(BaseModel):
    title: str
    is_visible: bool


class CountriesListForAdmin(CountriesList):
    model_config = ConfigDict(from_attributes=True)

    id: int
