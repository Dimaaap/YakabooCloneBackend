from pydantic import BaseModel, ConfigDict


class InterestingBase(BaseModel):
    title: str
    slug: str
    visible: bool = True


class InterestingCreate(InterestingBase):
    pass


class InterestingUpdate(InterestingCreate):
    pass


class InterestingUpdatePartial(InterestingUpdate):
    title: str | None = None
    slug: str | None = None
    visible: bool | None = None


class InterestingSchema(InterestingBase):
    model_config = ConfigDict(from_attributes=True)

    id: int