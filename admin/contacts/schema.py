from pydantic import BaseModel, ConfigDict


class Contacts(BaseModel):
    social_title: str
    link: str
    icon_title: str | None = None
    is_active: bool


class ContactsForAdminList(Contacts):
    model_config = ConfigDict(from_attributes=True)

    id: int