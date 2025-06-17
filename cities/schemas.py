from pydantic import BaseModel, ConfigDict


class CitiesBase(BaseModel):
    title: str
    is_visible: bool = True
    region: str
    country_id: int


class CitiesCreate(CitiesBase):
    pass


class CitiesUpdate(CitiesCreate):
    pass


class CitiesUpdatePartial(CitiesUpdate):
    title: str | None = None
    is_visible: bool | None = None
    region: str | None = None
    country_id: int | None = None


class CitiesSchema(CitiesBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
