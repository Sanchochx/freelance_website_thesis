"""add_empresa_to_users

Revision ID: 0001_add_empresa_to_users
Revises:
Create Date: 2026-03-05

Adds the `empresa` column to the users table for external client registration (US-002).
If starting from scratch, Base.metadata.create_all() in main.py already includes this
column — run this migration only when upgrading an existing database.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0001_add_empresa"
down_revision: Union[str, None] = "0000_create_users"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("empresa", sa.String(length=150), nullable=True))


def downgrade() -> None:
    op.drop_column("users", "empresa")
