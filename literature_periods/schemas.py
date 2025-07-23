from pydantic import BaseModel, ConfigDict

from core.models.literature_periods import PeriodTitleType


class LiteraturePeriodBase(BaseModel):
    title: PeriodTitleType
    slug: str


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