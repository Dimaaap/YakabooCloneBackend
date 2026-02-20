from pydantic import BaseModel, ConfigDict

from core.models.footer import FooterCategory


class Footers(BaseModel):
    title: str
    link: str
    category: FooterCategory
    active: bool


class FooterForAdminList(Footers):
    model_config = ConfigDict(from_attributes=True)

    id: int