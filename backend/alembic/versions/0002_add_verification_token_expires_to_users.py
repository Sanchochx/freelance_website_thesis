"""add_verification_token_expires_to_users

Revision ID: 0002_add_verification_token_expires_to_users
Revises: 0001_add_empresa_to_users
Create Date: 2026-03-05

Adds the `verification_token_expires` column to the users table for
24-hour token expiry (US-004 CA2).
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0002_add_verif_expires"
down_revision: Union[str, None] = "0001_add_empresa"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("verification_token_expires", sa.DateTime(timezone=True), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("users", "verification_token_expires")
