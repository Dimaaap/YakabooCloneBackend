from pydantic import BaseModel, ConfigDict


class CountriesList(BaseModel):
    title: str
    is_visible: bool


class CountriesListForAdmin(CountriesList):
    model_config = ConfigDict(from_attributes=True)

    id: int


class EditCountry(CountriesList):
    title: str | None = None
    is_visible: bool | None = None


class CreateCountry(CountriesList):
    ...
