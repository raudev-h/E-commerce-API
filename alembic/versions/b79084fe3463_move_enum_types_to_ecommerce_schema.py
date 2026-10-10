"""move enum types to ecommerce schema

The initial migration created `userrole` and `status` in `public`, but the app
connects with search_path = ecommerce, so inserts failed with
'type "userrole" does not exist'.

Revision ID: b79084fe3463
Revises: a3f2c1e9b047
Create Date: 2026-10-10 09:30:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'b79084fe3463'
down_revision: Union[str, Sequence[str], None] = 'a3f2c1e9b047'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

APP_SCHEMA = "ecommerce"
ENUM_TYPES: tuple[str, ...] = ("userrole", "status")


def upgrade() -> None:
    """Move enum types from public into the app schema (columns keep working: they reference the type by OID)."""
    for enum_type in ENUM_TYPES:
        op.execute(f"ALTER TYPE public.{enum_type} SET SCHEMA {APP_SCHEMA}")


def downgrade() -> None:
    """Move enum types back to public."""
    for enum_type in ENUM_TYPES:
        op.execute(f"ALTER TYPE {APP_SCHEMA}.{enum_type} SET SCHEMA public")
