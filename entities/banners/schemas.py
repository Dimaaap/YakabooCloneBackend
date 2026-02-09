from pydantic import BaseModel, ConfigDict


class BannerBase(BaseModel):
    image_src: str | None = None
    visible: bool = True
    link: str
    in_all_books_page: bool = False


class BannerCreate(BannerBase):
    pass


class BannerUpdate(BannerBase):
    pass


class BannerUpdatePartial(BannerUpdate):
    image_src: str | None = None
    visible: bool | None = None
    link: str | None = None
    in_all_books_page: bool | None = None


class BannerSchema(BannerBase):
    model_config = ConfigDict(from_attributes=True)

    id: int