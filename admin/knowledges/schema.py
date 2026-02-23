from pydantic import BaseModel, ConfigDict

class Knowledge(BaseModel):
    title: str
    slug: str
    container_title: str | None = None
    in_sidebar: bool = False
    is_active: bool = True
    content: str


class KnowledgeForAdminPageList(Knowledge):
    model_config = ConfigDict(from_attributes=True)