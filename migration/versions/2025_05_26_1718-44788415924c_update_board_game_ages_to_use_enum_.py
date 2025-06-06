"""update board_game_ages to use enum values, not keys

Revision ID: 44788415924c
Revises: ba46a2e02d27
Create Date: 2025-05-26 17:18:48.199747

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '44788415924c'
down_revision: Union[str, None] = 'ba46a2e02d27'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

old_enum_name = "age_enum"
tmp_enum_name = "age_enum_new"

new_enum_values = [
    "Підліткам",
    "Від 9 до 12 років",
    "Від 6 до 8 років",
    "Від 3 до 5 років",
    "Батькам",
    "До 2-х років"
]


def upgrade():
    op.execute(f"CREATE TYPE {tmp_enum_name} AS ENUM {tuple(new_enum_values)}")

    op.execute(f"ALTER TABLE board_game_ages ALTER COLUMN age TYPE {tmp_enum_name} USING age::text::{tmp_enum_name}")

    op.execute(f"DROP TYPE {old_enum_name}")

    op.execute(f"ALTER TYPE {tmp_enum_name} RENAME TO {old_enum_name}")


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    old_enum_values = [
        "TEENAGERS",
        "FROM_9_TO_12",
        "FROM_6_TO_8",
        "FROM_3_TO_5",
        "PARENTS",
        "TO_2_YEARS"
    ]

    # мапа значень value -> name
    value_to_name = {
        "Підліткам": "TEENAGERS",
        "Від 9 до 12 років": "FROM_9_TO_12",
        "Від 6 до 8 років": "FROM_6_TO_8",
        "Від 3 до 5 років": "FROM_3_TO_5",
        "Батькам": "PARENTS",
        "До 2-х років": "TO_2_YEARS"
    }

    old_enum_name = "age_enum"
    tmp_enum_name = "age_enum_old"

    # 1. Створити тимчасовий старий enum
    op.execute(f"CREATE TYPE {tmp_enum_name} AS ENUM {tuple(old_enum_values)}")

    # 2. Замінити значення у колонці на ключі enum (name)
    for val, name in value_to_name.items():
        op.execute(
            f"UPDATE board_game_ages SET age = '{name}' WHERE age = '{val}'"
        )

    # 3. Змінити тип age на новий тимчасовий enum
    op.execute(
        f"ALTER TABLE board_game_ages ALTER COLUMN age TYPE {tmp_enum_name} USING age::text::{tmp_enum_name}"
    )

    # 4. Видалити нову версію enum
    op.execute(f"DROP TYPE {old_enum_name}")

    # 5. Перейменувати тимчасовий enum назад
    op.execute(f"ALTER TYPE {tmp_enum_name} RENAME TO {old_enum_name}")
    # ### end Alembic commands ###