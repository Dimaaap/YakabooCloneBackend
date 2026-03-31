from pydantic import BaseModel, ConfigDict


class NewPostPostomatCommonFieldsMixin:
    address: str
    active: bool = True


class NewPostPostomats(BaseModel, NewPostPostomatCommonFieldsMixin):
    number: int
    city_title: str


class NewPostPostomatsForAdmin(NewPostPostomats):
    model_config = ConfigDict(from_attributes=True)

    id: int


class EditNewPostPostomat(BaseModel):
    address: str | None = None
    active: bool | None = None
    city_title: str | None = None


class CreateNewPostPostomat(BaseModel):
    address: str
    active: bool
    city_id: int