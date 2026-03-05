"""add_orders_table

Revision ID: 0004_add_orders_table
Revises: 0003_profile_services
Create Date: 2026-03-05

Creates orders table (stub — paquete/precio fields added in US-015).
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0004_add_orders_table"
down_revision: Union[str, None] = "0003_profile_services"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "orders",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "client_id",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "freelancer_id",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "service_id",
            sa.Integer(),
            sa.ForeignKey("services.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("estado", sa.String(30), nullable=False, server_default="pendiente"),
        sa.Column(
            "fecha_creacion",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
        ),
    )
    op.create_index("ix_orders_client_id", "orders", ["client_id"])
    op.create_index("ix_orders_freelancer_id", "orders", ["freelancer_id"])
    op.create_index("ix_orders_service_id", "orders", ["service_id"])


def downgrade() -> None:
    op.drop_table("orders")
