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