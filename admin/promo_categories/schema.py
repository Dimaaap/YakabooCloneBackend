from pydantic import BaseModel, ConfigDict


class PromoCategories(BaseModel):
    title: str
    slug: str
    is_active: bool = True


class PromoCategoriesForAdmin(PromoCategories):
    model_config = ConfigDict(from_attributes=True)