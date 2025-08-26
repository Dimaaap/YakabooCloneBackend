from pydantic import BaseModel, ConfigDict


class AccessoryBrandBase(BaseModel):
    title: str
    slug: str
    image: str | None = None
    #accessories: list[int] = []


class AccessoryBrandCreate(AccessoryBrandBase):
    pass


class AccessoryBrandUpdate(AccessoryBrandCreate):
    ...


class AccessoryBrandUpdatePartial(AccessoryBrandUpdate):
    title: str | None = None
    slug: str | None = None
    #accessories: list[int] | None = None


class AccessoryBrandSchema(AccessoryBrandBase):
    model_config = ConfigDict(from_attributes=True)

    id: int