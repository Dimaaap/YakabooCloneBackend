from pydantic import BaseModel, ConfigDict


class BookSeriaBase(BaseModel):
    title: str
    slug: str
    is_active: bool = True


class BookSeriaCreate(BookSeriaBase):
    ...


class BookSeriaUpdate(BookSeriaCreate):
    ...


class BookSeriaUpdatePartial(BookSeriaUpdate):
    title: str | None = None
    slug: str | None = None


class BookSeriaSchema(BookSeriaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    books_count: int = 0