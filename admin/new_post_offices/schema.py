from pydantic import BaseModel, ConfigDict


class NewPostOfficeCommonFieldsMixin:
    address: str
    active: bool = True
    weight_to: int | None = None


class NewPostOffices(BaseModel, NewPostOfficeCommonFieldsMixin):
    number: int
    city_title: str


class NewPostOfficesForAdmin(NewPostOffices):
    model_config = ConfigDict(from_attributes=True)

    id: int


class EditNewPostOffice(BaseModel):
    address: str | None = None
    active: bool | None = None
    weight_to: int | None = None
    city_title: str | None = None


class CreateNewPostOffice(BaseModel):
    address: str
    active: bool
    weight_to: int | None = None
    city_id: int