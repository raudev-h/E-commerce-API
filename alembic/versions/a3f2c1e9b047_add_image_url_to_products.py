"""add image_url to products

Revision ID: a3f2c1e9b047
Revises: 8d17df6a933a
Create Date: 2026-04-09 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a3f2c1e9b047'
down_revision: Union[str, Sequence[str], None] = '8d17df6a933a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'products',
        sa.Column('image_url', sa.String(length=500), nullable=True),
        schema='ecommerce'
    )


def downgrade() -> None:
    op.drop_column('products', 'image_url', schema='ecommerce')
