from pydantic import BaseModel, ConfigDict


class AccessoriesLiteSchema(BaseModel):
    id: int
    title: str
    slug: str

    model_config = ConfigDict(from_attributes=True)


class AccessoryCategoryBase(BaseModel):
    title: str
    slug: str
    images_src: list[str] = []


class AccessoryCategoryCreate(AccessoryCategoryBase):
    ...


class AccessoryCategoryUpdate(AccessoryCategoryBase):
    ...


class AccessoryCategoryUpdatePartial(AccessoryCategoryUpdate):
    title: str | None = None
    slg: str | None = None
    images_src: list[str] | None = None


class AccessoryCategorySchema(AccessoryCategoryBase):
    model_config = ConfigDict(from_attributes=True)

    id: int