"""changed tables

Revision ID: 3600e716661f
Revises: bab53be851c4
Create Date: 2026-08-31 19:31:26.306467

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "3600e716661f"
down_revision: Union[str, Sequence[str], None] = "bab53be851c4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint(
        "exercise_sets_exercise_id_fkey",
        "exercise_sets",
        type_="foreignkey",
    )

    op.drop_index(
        "ix_exercise_sets_exercise_id",
        table_name="exercise_sets",
    )

    op.drop_column(
        "exercise_sets",
        "exercise_id",
    )

    op.add_column(
        "exercise_sets",
        sa.Column(
            "exercise_name",
            sa.String(),
            nullable=False,
        ),
    )

    op.create_index(
        "ix_exercise_sets_exercise_name",
        "exercise_sets",
        ["exercise_name"],
        unique=False,
    )

    op.drop_table("exercise_types")


def downgrade() -> None:
    # 1. alte exercise_types Tabelle wiederherstellen
    op.create_table(
        "exercise_types",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("exercise_name", sa.VARCHAR(), nullable=False),
        sa.Column("exercise_name_normalized", sa.VARCHAR(), nullable=False),
        sa.PrimaryKeyConstraint(
            "id",
            name=op.f("exercise_types_pkey"),
        ),
        sa.UniqueConstraint(
            "exercise_name",
            name=op.f("exercise_types_exercise_name_key"),
        ),
        sa.UniqueConstraint(
            "exercise_name_normalized",
            name=op.f("exercise_types_exercise_name_normalized_key"),
        ),
    )

    # 2. exercise_id wieder hinzufügen
    op.add_column(
        "exercise_sets",
        sa.Column(
            "exercise_id",
            sa.UUID(),
            nullable=False,
        ),
    )

    # 3. Index wieder erstellen
    op.create_index(
        op.f("ix_exercise_sets_exercise_id"),
        "exercise_sets",
        ["exercise_id"],
        unique=False,
    )

    # 4. FK kann jetzt erstellt werden
    op.create_foreign_key(
        op.f("exercise_sets_exercise_id_fkey"),
        "exercise_sets",
        "exercise_types",
        ["exercise_id"],
        ["id"],
    )

    # 5. neue exercise_name-Struktur entfernen
    op.drop_index(
        op.f("ix_exercise_sets_exercise_name"),
        table_name="exercise_sets",
    )

    op.drop_column(
        "exercise_sets",
        "exercise_name",
    )
