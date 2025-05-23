from pydantic import BaseModel, ConfigDict


class GameBrandBase(BaseModel):
    title: str
    slug: str
    image: str | None = None
    description: str | None = None
    visible: bool = True
    board_games: list[int] = []


class GameBrandCreate(GameBrandBase):
    pass


class GameBrandUpdate(GameBrandCreate):
    pass


class GameBrandUpdatePartial(GameBrandUpdate):
    title: str | None = None
    slug: str | None = None
    visible: bool | None = None
    board_games: list[int] | None = None


class GameBrandSchema(GameBrandBase):
    model_config = ConfigDict(from_attributes=True)

    id: int