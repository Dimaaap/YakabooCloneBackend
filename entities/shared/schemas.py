from pydantic import BaseModel, ConfigDict


class CategoryShortSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    slug: str


class SubcategoryShortSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    slug: str
    category: CategoryShortSchema



class DoubleSubcategoryShortSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    slug: str
    subcategory: SubcategoryShortSchema