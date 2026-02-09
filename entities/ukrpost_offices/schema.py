from pydantic import BaseModel, ConfigDict


class UkrpostOfficeBase(BaseModel):
    office_number: int
    address: str
    active: bool = True
    number_in_city: int
    id: int

    city_id: int


class UkrpostOfficeCreate(UkrpostOfficeBase):
    pass


class UkrpostOfficeUpdate(UkrpostOfficeCreate):
    pass


class UkrpostOfficeUpdatePartial(UkrpostOfficeUpdate):
    office_number: int | None = None
    address: str | None = None
    active: bool | None = True
    number_in_city: int | None = None

    city_id: int | None = None


class UkrpostOfficeSchema(UkrpostOfficeBase):
    model_config = ConfigDict(from_attributes=True)

    id: int