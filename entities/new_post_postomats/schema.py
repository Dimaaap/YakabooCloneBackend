from pydantic import BaseModel, ConfigDict


class NewPostPostomatBase(BaseModel):
    number: int
    address: str
    active: bool = True

    city_id: int
    id: int


class NewPostPostomatCreate(NewPostPostomatBase):
    ...


class NewPostPostomatUpdate(NewPostPostomatCreate):
    ...


class NewPostPostomatUpdatePartial(NewPostPostomatUpdate):
    number: int | None = None
    address: str | None = None

    city_id: int | None = None


class NewPostPostomatSchema(NewPostPostomatBase):
    model_config = ConfigDict(from_attributes=True)
