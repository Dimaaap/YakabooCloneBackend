from pydantic import BaseModel, ConfigDict


class GameSeriaBase(BaseModel):
    title: str
    slug: str
    board_games: list[int] | None = None


class GameSeriaCreate(GameSeriaBase):
    pass


class GameSeriaUpdate(GameSeriaCreate):
    pass


class GameSeriaUpdatePartial(GameSeriaUpdate):
    title: str | None = None
    slug: str | None = None
    board_games: list[int] | None = None


class GameSeriaSchema(GameSeriaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
