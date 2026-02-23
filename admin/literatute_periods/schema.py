from pydantic import BaseModel, ConfigDict

from core.models.literature_periods import PeriodTitleType


class LiteraturePeriods(BaseModel):
    title: PeriodTitleType
    slug: str


class LiteraturePeriodForAdminList(LiteraturePeriods):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    id: int