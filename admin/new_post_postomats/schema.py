from pydantic import BaseModel, ConfigDict


class NewPostPostomats(BaseModel):
    number: int
    address: str
    active: bool = True
    city_title: str


class NewPostPostomatsForAdmin(NewPostPostomats):
    model_config = ConfigDict(from_attributes=True)

    id: int