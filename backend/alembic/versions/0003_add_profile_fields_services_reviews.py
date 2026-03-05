"""add_profile_fields_services_reviews

Revision ID: 0003_add_profile_fields_services_reviews
Revises: 0002_add_verification_token_expires_to_users
Create Date: 2026-03-05

Adds portafolio and badges columns to users table.
Creates services table (no FK to categories — stub).
Creates reviews table (no FK to orders — stub).
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "0003_profile_services"
down_revision: Union[str, None] = "0002_add_verif_expires"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # --- users: new profile columns ---
    op.add_column(
        "users",
        sa.Column("portafolio", postgresql.ARRAY(sa.String()), nullable=True),
    )
    op.add_column(
        "users",
        sa.Column("badges", postgresql.ARRAY(sa.String()), nullable=True),
    )

    # --- services table ---
    op.create_table(
        "services",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "user_id",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("titulo", sa.String(200), nullable=False),
        sa.Column("descripcion", sa.Text(), nullable=True),
        sa.Column("precio_basico", sa.Numeric(10, 2), nullable=True),
        sa.Column("precio_estandar", sa.Numeric(10, 2), nullable=True),
        sa.Column("precio_premium", sa.Numeric(10, 2), nullable=True),
        sa.Column("tiempo_entrega", sa.Integer(), nullable=True),
        sa.Column("imagenes", postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column("categoria_id", sa.Integer(), nullable=True),  # no FK — categories table doesn't exist yet
        sa.Column("estado", sa.String(20), nullable=False, server_default="activo"),
        sa.Column(
            "fecha_creacion",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
        ),
    )
    op.create_index("ix_services_user_id", "services", ["user_id"])

    # --- reviews table ---
    op.create_table(
        "reviews",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "reviewer_id",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "reviewed_id",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("order_id", sa.Integer(), nullable=True),  # no FK — orders table doesn't exist yet
        sa.Column("rating", sa.Numeric(2, 1), nullable=False),
        sa.Column("comentario", sa.Text(), nullable=True),
        sa.Column(
            "fecha",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
        ),
    )
    op.create_index("ix_reviews_reviewer_id", "reviews", ["reviewer_id"])
    op.create_index("ix_reviews_reviewed_id", "reviews", ["reviewed_id"])


def downgrade() -> None:
    op.drop_table("reviews")
    op.drop_table("services")
    op.drop_column("users", "badges")
    op.drop_column("users", "portafolio")
