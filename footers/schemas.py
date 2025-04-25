from pydantic import BaseModel, ConfigDict
from core.models.footer import FooterCategory


class FooterBase(BaseModel):
    title: str
    link: str | None = None
    category: FooterCategory = FooterCategory.YAKABOO
    active: bool = True


class FooterCreate(FooterBase):
    pass


class FooterUpdate(FooterCreate):
    pass


class FooterUpdatePartial(FooterUpdate):
    title: str | None = None
    category: FooterCategory | None = None
    active: bool | None = None


class FooterSchema(FooterBase):
    model_config = ConfigDict(from_attributes=True,
                              use_enum_values=True)

    id: int