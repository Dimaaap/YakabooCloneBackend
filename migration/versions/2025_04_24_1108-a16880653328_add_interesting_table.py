"""Add interesting table

Revision ID: a16880653328
Revises: 4d93ec840333
Create Date: 2025-04-24 11:08:13.114791

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a16880653328'
down_revision: Union[str, None] = '4d93ec840333'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('interesting',
    sa.Column('title', sa.String(length=100), server_default='', nullable=False),
    sa.Column('slug', sa.String(length=100), server_default='', nullable=False),
    sa.Column('visible', sa.Boolean(), server_default='1', nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('interesting')
    # ### end Alembic commands ###