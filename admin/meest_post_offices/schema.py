from pydantic import BaseModel, ConfigDict


class MeestPostOffices(BaseModel):
    office_number: int
    address: str
    active: bool = True
    city_title: str


class MeestPostOfficesForAdmin(MeestPostOffices):
    model_config = ConfigDict(from_attributes=True)

    id: int


class EditMeestPostOffice(MeestPostOffices):
    office_number: int | None = None
    address: str | None = None
    active: bool | None = None
    city_title: str | None = None