from datetime import datetime

from pydantic import BaseModel, ConfigDict


class MainPageTitle(BaseModel):
    title: str
    active: bool = True
    created_at: datetime | None = None
    updated_at: datetime | None = None


class MainPageTitlesListForAdmin(MainPageTitle):
    model_config = ConfigDict(from_attributes=True)

    id: int