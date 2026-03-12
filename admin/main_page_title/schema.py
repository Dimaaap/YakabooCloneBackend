from datetime import datetime

from pydantic import BaseModel, ConfigDict


class MainPageTitle(BaseModel):
    title: str
    active: bool = True


class MainPageTitlesListForAdmin(MainPageTitle):
    model_config = ConfigDict(from_attributes=True)

    id: int


class EditMainPageTitle(MainPageTitle):
    title: str | None = None
    active: bool | None = None