from pydantic import BaseModel, ConfigDict


class HobbyBrandBase(BaseModel):
    title: str
    slug: str
    image: str | None = None
    description: str | None = None
    visible: bool = True
    #hobbies: list[int] = []


class HobbyBrandCreate(HobbyBrandBase):
    pass


class HobbyBrandUpdate(HobbyBrandCreate):
    ...


class HobbyBrandUpdatePartial(HobbyBrandUpdate):
    title: str | None = None
    slug: str | None = None
    visible: bool | None = None
    #hobbies: list[int] | None = None


class HobbyBrandSchema(HobbyBrandBase):
    model_config = ConfigDict(from_attributes=True)

    id: int