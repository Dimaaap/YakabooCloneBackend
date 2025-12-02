from pydantic import BaseModel, ConfigDict


class NewPostOfficeBase(BaseModel):
    number: int
    address: str
    active: bool = True
    weight_to: int | None = None

    city_id: int
    id: int


class NewPostOfficeCreate(NewPostOfficeBase):
    ...


class NewPostOfficeUpdate(NewPostOfficeCreate):
    ...


class NewPostOfficeUpdatePartial(NewPostOfficeUpdate):
    number: int | None = None
    address: str | None = None

    city_id: int | None = None


class NewPostOfficeSchema(NewPostOfficeBase):
    model_config = ConfigDict(from_attributes=True)