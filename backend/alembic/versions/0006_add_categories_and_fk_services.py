"""add_categories_and_fk_services

Revision ID: 0006_add_categories
Revises: 0005_add_reset_token
Create Date: 2026-03-05

Creates categories table, seeds 8 default categories, and adds FK constraint
on services.categoria_id — US-009 CA6.
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0006_add_categories"
down_revision: Union[str, None] = "0005_add_reset_token"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

CATEGORIES = [
    (1, "Diseño Gráfico", "palette"),
    (2, "Programación y Tecnología", "code"),
    (3, "Marketing Digital", "megaphone"),
    (4, "Redacción y Contenido", "pencil"),
    (5, "Video y Animación", "film"),
    (6, "Música y Audio", "music"),
    (7, "Fotografía", "camera"),
    (8, "Consultoría y Asesoría", "briefcase"),
]


def upgrade() -> None:
    # Create categories table
    op.create_table(
        "categories",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("nombre", sa.String(100), nullable=False),
        sa.Column("icono", sa.String(50), nullable=True),
    )

    # Seed default categories
    categories_table = sa.table(
        "categories",
        sa.column("id", sa.Integer),
        sa.column("nombre", sa.String),
        sa.column("icono", sa.String),
    )
    op.bulk_insert(
        categories_table,
        [{"id": cat_id, "nombre": nombre, "icono": icono} for cat_id, nombre, icono in CATEGORIES],
    )

    # Add FK constraint on services.categoria_id → categories.id
    op.create_foreign_key(
        "fk_services_categoria_id",
        "services",
        "categories",
        ["categoria_id"],
        ["id"],
        ondelete="SET NULL",
    )


def downgrade() -> None:
    op.drop_constraint("fk_services_categoria_id", "services", type_="foreignkey")
    op.drop_table("categories")
