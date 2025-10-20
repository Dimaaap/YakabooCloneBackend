from pydantic import BaseModel, ConfigDict


class BookIllustratorBase(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    slug: str
    is_active: bool = True


class BookIllustratorCreate(BookIllustratorBase):
    ...


class BookIllustratorUpdate(BookIllustratorCreate):
    ...


class BookIllustratorUpdatePartial(BookIllustratorUpdate):
    slug: str | None = None


class BookIllustratorSchema(BookIllustratorBase):
    model_config = ConfigDict(from_attributes=True)

    id: int