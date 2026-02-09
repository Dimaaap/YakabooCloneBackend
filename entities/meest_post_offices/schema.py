from pydantic import BaseModel, ConfigDict


class MeestPostOfficeBase(BaseModel):
    office_number: int
    address: str
    active: bool = True

    city_id: int
    id: int


class MeestPostOfficeCreate(MeestPostOfficeBase):
    ...


class MeestPostOfficeUpdate(MeestPostOfficeCreate):
    ...


class MeestPostOfficeUpdatePartial(MeestPostOfficeUpdate):
    office_number: int | None = None
    address: str | None = None
    active: bool | None = None

    city_id: int | None = None


class MeestPostOfficeSchema(MeestPostOfficeBase):
    model_config = ConfigDict(from_attributes=True)

    id: int