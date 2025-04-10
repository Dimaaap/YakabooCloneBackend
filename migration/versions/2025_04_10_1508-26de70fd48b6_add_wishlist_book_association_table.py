"""Add wishlist_book_association table

Revision ID: 26de70fd48b6
Revises: 
Create Date: 2025-04-10 15:08:59.991786

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '26de70fd48b6'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('authors',
    sa.Column('first_name', sa.String(length=255), server_default='', nullable=False),
    sa.Column('last_name', sa.String(length=255), server_default='', nullable=False),
    sa.Column('slug', sa.String(length=255), server_default='', nullable=False),
    sa.Column('date_of_birth', sa.Date(), nullable=True),
    sa.Column('description', sa.Text(), server_default='', nullable=False),
    sa.Column('is_active', sa.Boolean(), server_default='1', nullable=False),
    sa.Column('short_description', sa.Text(), server_default='', nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('banners',
    sa.Column('image_src', sa.String(length=255), server_default='', nullable=False),
    sa.Column('visible', sa.Boolean(), server_default='1', nullable=False),
    sa.Column('link', sa.String(length=255), server_default='', nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('book_info',
    sa.Column('in_stock', sa.Boolean(), server_default='1', nullable=False),
    sa.Column('visible', sa.Boolean(), server_default='1', nullable=False),
    sa.Column('code', sa.Integer(), nullable=False),
    sa.Column('rate', sa.Float(), server_default='0', nullable=False),
    sa.Column('illustrations', sa.String(length=255), server_default='', nullable=False),
    sa.Column('ISBN', sa.String(length=255), server_default='', nullable=False),
    sa.Column('cover_type', sa.Enum('SOLID', 'SOFT', name='covertypes'), server_default='SOLID', nullable=False),
    sa.Column('pages_count', sa.Integer(), server_default='0', nullable=False),
    sa.Column('is_has_cashback', sa.Boolean(), server_default='1', nullable=False),
    sa.Column('is_has_esupport', sa.Boolean(), server_default='1', nullable=False),
    sa.Column('format', sa.Enum('PAPER', 'ELECTRONIC', 'AUDIO', name='bookformats'), server_default='PAPER', nullable=False),
    sa.Column('language', sa.Enum('UKRAINIAN', 'ENGLISH', name='booklanguages'), server_default='UKRAINIAN', nullable=False),
    sa.Column('publishing_year', sa.Integer(), server_default='0', nullable=False),
    sa.Column('first_published_at', sa.Integer(), server_default='0', nullable=False),
    sa.Column('description', sa.Text(), server_default='', nullable=False),
    sa.Column('characteristics', sa.Text(), server_default='', nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('code')
    )
    op.create_table('categories',
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('slug', sa.String(length=100), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('slug'),
    sa.UniqueConstraint('title')
    )
    op.create_table('email_subs',
    sa.Column('email', sa.String(length=110), nullable=False),
    sa.Column('date_sub', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('knowledges',
    sa.Column('title', sa.String(length=100), server_default='', nullable=False),
    sa.Column('slug', sa.String(length=100), server_default='', nullable=False),
    sa.Column('is_active', sa.Boolean(), server_default='1', nullable=False),
    sa.Column('content', sa.Text(), server_default='', nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
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
    op.create_table('users',
    sa.Column('first_name', sa.String(length=155), server_default='', nullable=False),
    sa.Column('last_name', sa.String(length=155), server_default='', nullable=False),
    sa.Column('phone_number', sa.String(length=11), nullable=False),
    sa.Column('email', sa.String(length=80), nullable=False),
    sa.Column('password', sa.String(length=80), nullable=False),
    sa.Column('is_staff', sa.Boolean(), server_default='0', nullable=False),
    sa.Column('is_active', sa.Boolean(), server_default='1', nullable=False),
    sa.Column('is_verified', sa.Boolean(), server_default='0', nullable=False),
    sa.Column('is_subscribed_to_news', sa.Boolean(), server_default='0', nullable=False),
    sa.Column('birth_date', sa.Date(), nullable=True),
    sa.Column('date_joined', sa.DateTime(), server_default='2025-04-10 15:08:59.718785', nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('phone_number')
    )
    op.create_table('books',
    sa.Column('title', sa.String(length=255), server_default='', nullable=False),
    sa.Column('slug', sa.String(length=255), server_default='', nullable=False),
    sa.Column('price', sa.Integer(), server_default='0', nullable=False),
    sa.Column('book_info_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['book_info_id'], ['book_info.id'], name='fk_book_info'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sub_categories',
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('slug', sa.String(length=100), nullable=False),
    sa.Column('is_visible', sa.Boolean(), server_default='1', nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('slug'),
    sa.UniqueConstraint('title')
    )
    op.create_table('wishlists',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('author_book_association',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('author_id', sa.Integer(), nullable=False),
    sa.Column('book_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['author_id'], ['authors.id'], ),
    sa.ForeignKeyConstraint(['book_id'], ['books.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('author_id', 'book_id', name='idx_unique_author_book')
    )
    op.create_table('subcategory_book_association',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('subcategory_id', sa.Integer(), nullable=False),
    sa.Column('book_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['book_id'], ['books.id'], ),
    sa.ForeignKeyConstraint(['subcategory_id'], ['sub_categories.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('book_id', 'subcategory_id', name='idx_unique_subcategory_book')
    )
    op.create_table('wishlist_book_association',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('book_id', sa.Integer(), nullable=False),
    sa.Column('wishlist_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['book_id'], ['books.id'], ),
    sa.ForeignKeyConstraint(['wishlist_id'], ['wishlists.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('wishlist_book_association')
    op.drop_table('subcategory_book_association')
    op.drop_table('author_book_association')
    op.drop_table('wishlists')
    op.drop_table('sub_categories')
    op.drop_table('books')
    op.drop_table('users')
    op.drop_table('sidebars')
    op.drop_table('knowledges')
    op.drop_table('email_subs')
    op.drop_table('categories')
    op.drop_table('book_info')
    op.drop_table('banners')
    op.drop_table('authors')
    # ### end Alembic commands ###