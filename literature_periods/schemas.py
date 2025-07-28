from pydantic import BaseModel, ConfigDict

from core.models.literature_periods import PeriodTitleType
from typing import TYPE_CHECKING



class LiteraturePeriodBase(BaseModel):
    title: PeriodTitleType
    slug: str


class LiteraturePeriodWithCountSchema(BaseModel):
    id: int
    title: str
    slug: str
    books_count: int

    model_config = ConfigDict(from_attributes=True)


class LiteraturePeriodCreate(LiteraturePeriodBase):
    ...


class LiteraturePeriodUpdate(LiteraturePeriodCreate):
    ...


class LiteraturePeriodUpdatePartial(LiteraturePeriodUpdate):
    title: PeriodTitleType | None = None
    slug: str | None = None


class LiteraturePeriodSchema(LiteraturePeriodBase):
    model_config = ConfigDict(from_attributes=True)

    id: int