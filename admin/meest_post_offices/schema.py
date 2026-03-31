from pydantic import BaseModel, ConfigDict


class MeestPostOfficeCommonFieldsMixin:
    office_number: int
    address: str
    active: bool = True


class MeestPostOffices(BaseModel,MeestPostOfficeCommonFieldsMixin):
    city_title: str


class MeestPostOfficesForAdmin(MeestPostOffices):
    model_config = ConfigDict(from_attributes=True)

    id: int


class EditMeestPostOffice(BaseModel):
    address: str | None = None
    active: bool | None = None
    city_title: str | None = None


class CreateMeestPostOffice(BaseModel):
    address: str
    active: bool
    city_id: int