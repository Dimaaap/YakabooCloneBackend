from pydantic import BaseModel, ConfigDict


class PromoCategoryBase(BaseModel):
    title: str
    slug: str
    is_active: bool = True


class PromoCategoryCreate(PromoCategoryBase):
    pass


class PromoCategoryUpdate(PromoCategoryCreate):
    pass


class PromoCategoryUpdatePartial(PromoCategoryUpdate):
    title: str | None = None
    slug: str | None = None
    is_active: bool | None = True


class PromoCategorySchema(PromoCategoryBase):
    model_config = ConfigDict(from_attributes=True)

    id: int