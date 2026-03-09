from pydantic import BaseModel, ConfigDict


class UkrpostOffices(BaseModel):
    office_number: int
    address: str
    active: bool = True

    city_title: str


class UkrpostOfficesForAdmin(UkrpostOffices):
    model_config = ConfigDict(from_attributes=True)

    id: int


class EditUkrpostOffice(UkrpostOffices):
    office_number: int | None = None
    address: str | None = None
    active: bool | None = None
    city_title: str | None = None