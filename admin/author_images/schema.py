from pydantic import BaseModel, ConfigDict


class AuthorImages(BaseModel):
    image_path: str
    author_name: str


class AuthorImagesForAdminPage(AuthorImages):
    model_config = ConfigDict(from_attributes=True)

    id: int