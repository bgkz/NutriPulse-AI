"""change nutrition id to uuid

Revision ID: 845c4044b300
Revises: 470ff440b718
Create Date: 2026-08-31 15:09:54.738818

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "845c4044b300"
down_revision: Union[str, Sequence[str], None] = "470ff440b718"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint(
        "nutritions_pkey",
        "nutritions",
        type_="primary",
    )

    op.drop_column("nutritions", "id")

    op.add_column(
        "nutritions",
        sa.Column(
            "id",
            sa.Uuid(),
            nullable=False,
        ),
    )

    op.create_primary_key(
        "nutritions_pkey",
        "nutritions",
        ["id"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "nutritions_pkey",
        "nutritions",
        type_="primary",
    )

    op.drop_column("nutritions", "id")

    op.add_column(
        "nutritions",
        sa.Column(
            "id",
            sa.Integer(),
            nullable=False,
        ),
    )

    op.create_primary_key(
        "nutritions_pkey",
        "nutritions",
        ["id"],
    )
