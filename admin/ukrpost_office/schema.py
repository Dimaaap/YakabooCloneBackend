from pydantic import BaseModel, ConfigDict


class UkrpostOffices(BaseModel):
    office_number: int
    address: str
    active: bool = True

    city_title: str


class UkrpostOfficesForAdmin(UkrpostOffices):
    model_config = ConfigDict(from_attributes=True)

    id: int
