from pydantic import BaseModel, ConfigDict


class KnowledgeBase(BaseModel):
    title: str
    slug: str
    is_active: bool
    content: str


class KnowledgeCreate(KnowledgeBase):
    pass


class KnowledgeUpdate(KnowledgeCreate):
    pass


class KnowledgeUpdatePartial(KnowledgeUpdate):
    title: str | None = None
    slug: str | None = None
    is_active: bool | None = None
    content: str | None = None


class KnowledgeSchema(KnowledgeBase):
    model_config = ConfigDict(from_attributes=True)

    id: int