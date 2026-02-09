from pydantic import BaseModel, ConfigDict


class ContactsBase(BaseModel):
    social_title: str
    link: str | None = None
    icon_title: str | None = None
    is_active: bool = True


class ContactsCreate(ContactsBase):
    pass


class ContactsUpdate(ContactsCreate):
    pass


class ContactsUpdatePartial(ContactsUpdate):
    social_title: str | None = None
    is_active: bool | None = None


class ContactsSchema(ContactsBase):
    model_config = ConfigDict(from_attributes=True)

    id: int