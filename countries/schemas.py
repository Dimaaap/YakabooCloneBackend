from pydantic import BaseModel, ConfigDict

from cities.schemas import CitiesSchema


class CountriesBase(BaseModel):
    title: str
    is_visible: bool = True
    cities: list[CitiesSchema] = []


class CountriesCreate(CountriesBase):
    pass


class CountriesUpdate(CountriesCreate):
    pass


class CountriesUpdatePartial(CountriesUpdate):
    title: str | None = None
    is_active: bool | None = None
    cities: list[int] | None = None


class CountriesSchema(CountriesBase):
    model_config = ConfigDict(from_attributes=True)

    id: int