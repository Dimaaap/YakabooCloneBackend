from pydantic import BaseModel, ConfigDict


class BookTranslatorBase(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    slug: str
    is_active: bool = True


class BookTranslatorCreate(BookTranslatorBase):
    ...


class BookTranslatorUpdate(BookTranslatorCreate):
    ...


class BookTranslatorUpdatePartial(BookTranslatorUpdate):
    slug: str | None = None


class BookTranslatorSchema(BookTranslatorBase):
    model_config = ConfigDict(from_attributes=True)

    id: int