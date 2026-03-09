from pydantic import BaseModel, ConfigDict


class Sidebars(BaseModel):
    title: str
    slug: str
    icon: str | None = None
    visible: bool = True
    order_number: int
    is_clickable: bool = False
    link: str = ""


class SidebarsForAdminPage(Sidebars):
    model_config = ConfigDict(from_attributes=True)

    id: int


class EditSidebar(Sidebars):
    title: str | None = None
    slug: str | None = None
    order_number: int | None = None
    link: str | None = None