"""Create sidebar table

Revision ID: ec99324640ce
Revises: 
Create Date: 2025-04-04 21:12:31.401239

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ec99324640ce'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sidebars',
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('slug', sa.String(length=110), nullable=False),
    sa.Column('icon', sa.String(length=255), server_default='', nullable=False),
    sa.Column('visible', sa.Boolean(), server_default='1', nullable=False),
    sa.Column('order_number', sa.Integer(), server_default='1', nullable=False),
    sa.Column('is_clickable', sa.Boolean(), server_default='0', nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('slug'),
    sa.UniqueConstraint('title')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sidebars')
    # ### end Alembic commands ###