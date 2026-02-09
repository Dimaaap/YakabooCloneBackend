from pydantic import BaseModel, ConfigDict


class BookEditionGroupBase(BaseModel):
    title: str | None = None
    description: str | None = None



class BookEditionGroupCreate(BookEditionGroupBase):
    ...


class BookEditionGroupUpdate(BookEditionGroupCreate):
    ...


class BookEditionGroupUpdatePartial(BookEditionGroupUpdate):
    ...


class BookEditionGroupSchema(BookEditionGroupBase):
    model_config = ConfigDict(from_attributes=True)

    id: int