from datetime import datetime

from pydantic import BaseModel, ConfigDict


class MainPageTitleBase(BaseModel):
    title: str
    active: bool = True


class MainPageTitleCreate(MainPageTitleBase):
    active: bool | None = None


class MainPageTitleUpdate(MainPageTitleCreate):
    ...


class MainPageTitleUpdatePartial(MainPageTitleUpdate):
    title: str | None


class MainPageTitleSchema(MainPageTitleBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime