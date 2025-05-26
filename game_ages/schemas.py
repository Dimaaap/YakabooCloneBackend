from pydantic import BaseModel, ConfigDict

from core.models.board_game_ages import Age


class GameAgeBase(BaseModel):
    age: Age
    slug: str
    board_game: list[int] = []


class GameAgeCreate(GameAgeBase):
    pass


class GameAgeUpdate(GameAgeCreate):
    pass


class GameAgeUpdatePartial(GameAgeUpdate):
    age: Age | None = None
    slug: str | None = None
    board_game: list[int] | None = None


class GameAgeSchema(GameAgeBase):
    model_config = ConfigDict(from_attributes=True)

    id: int