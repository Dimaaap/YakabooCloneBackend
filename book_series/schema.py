from pydantic import BaseModel, ConfigDict, conint


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


class BookFilters(BaseModel):
    limit: conint(ge=1, le=100) = 100
    offset: conint(ge=0) = 0
    categories: list[str] | None = None
    publishers: list[str] | None = None
    languages: list[str] | None = None
    bookTypes: list[str] | None = None
    authors: list[str] | None = None
    series: list[str] | None = None
    in_stock: bool | None = None
    price_min: int | None = None
    price_max: int | None = None
    filters: list[str] | None = None
