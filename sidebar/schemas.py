from pydantic import BaseModel, ConfigDict


class SidebarBase(BaseModel):
    title: str
    slug: str
    icon: str | None = None
    visible: bool
    order_number: int
    is_clickable: bool
    link: str


class SidebarCreate(SidebarBase):
    pass


class SidebarUpdate(SidebarCreate):
    pass


class SidebarUpdatePartial(SidebarUpdate):
    title: str | None = None
    slug: str | None = None
    icon: str | None = None
    visible: bool | None = None
    order_number: int | None = None
    is_clickable: bool | None = None
    link: str | None = None


class Sidebar(SidebarBase):
    model_config = ConfigDict(from_attributes=True)

    id: int 