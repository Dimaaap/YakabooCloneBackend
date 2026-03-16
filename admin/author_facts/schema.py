from pydantic import BaseModel, ConfigDict


class AuthorFacts(BaseModel):
    fact_text: str

    author_name: str
    author_id: int


class AuthorFactsForAdminPage(AuthorFacts):
    model_config = ConfigDict(from_attributes=True)

    id: int


class EditAuthorFact(AuthorFacts):
    fact_text: str | None = None
    author_name: str | None = None


class CreateAuthorFact(BaseModel):
    fact_text: str
    author_id: int