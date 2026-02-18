from pydantic import BaseModel, ConfigDict


class BannersList(BaseModel):
    image_src: str
    visible: bool
    link: str = ""
    in_all_books_page: bool


class BannersListForAdmin(BannersList):
    model_config = ConfigDict(from_attributes=True)

    id: int