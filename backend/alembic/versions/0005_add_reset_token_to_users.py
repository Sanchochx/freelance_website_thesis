"""add_reset_token_to_users

Revision ID: 0005_add_reset_token
Revises: 0004_add_orders_table
Create Date: 2026-03-05

Adds reset_token and reset_token_expires columns to users table — US-008.
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0005_add_reset_token"
down_revision: Union[str, None] = "0004_add_orders_table"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("reset_token", sa.String(255), nullable=True))
    op.add_column("users", sa.Column("reset_token_expires", sa.DateTime(timezone=True), nullable=True))


def downgrade() -> None:
    op.drop_column("users", "reset_token_expires")
    op.drop_column("users", "reset_token")
