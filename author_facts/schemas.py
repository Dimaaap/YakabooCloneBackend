from pydantic import BaseModel, ConfigDict


class AuthorFactBase(BaseModel):
    fact_text: str | None = None
    author_id: int


class AuthorFactCreate(AuthorFactBase):
    ...


class AuthorFactUpdate(AuthorFactCreate):
    ...


class AuthorFactUpdatePartial(AuthorFactUpdate):
    author_id: int | None = None


class AuthorFactSchema(AuthorFactBase):
    model_config = ConfigDict(from_attributes=True)

    id: int