from pydantic import BaseModel, ConfigDict


class NewPostOffices(BaseModel):
    number: int
    address: str
    active: bool = True
    weight_to: int | None = None
    city_title: str


class NewPostOfficesForAdmin(NewPostOffices):
    model_config = ConfigDict(from_attributes=True)

    id: int


class EditNewPostOffice(BaseModel):
    address: str | None = None
    active: bool | None = None
    weight_to: int | None = None
    city_title: str | None = None