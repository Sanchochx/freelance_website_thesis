"""create_users_table

Revision ID: 0000_create_users_table
Revises:
Create Date: 2026-03-05

Initial migration: creates the users table with all base columns.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "0000_create_users"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("nombre", sa.String(100), nullable=False),
        sa.Column("email", sa.String(150), unique=True, nullable=False, index=True),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("rol", sa.String(20), nullable=False),
        sa.Column("carrera", sa.String(100), nullable=True),
        sa.Column("semestre", sa.Integer(), nullable=True),
        sa.Column("avatar_url", sa.String(255), nullable=True),
        sa.Column("bio", sa.Text(), nullable=True),
        sa.Column("habilidades", postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column("wallet_balance", sa.Numeric(12, 2), server_default="0"),
        sa.Column("verificado", sa.Boolean(), server_default="false"),
        sa.Column("verification_token", sa.String(255), nullable=True),
        sa.Column(
            "fecha_registro",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
        ),
    )


def downgrade() -> None:
    op.drop_table("users")
