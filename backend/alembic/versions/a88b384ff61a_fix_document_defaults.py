"""fix document defaults

Revision ID: a88b384ff61a
Revises: f97dd32ad97d
Create Date: 2026-09-15 22:02:23.496830

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a88b384ff61a"
down_revision: Union[str, Sequence[str], None] = "f97dd32ad97d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "documents",
        "processing_status",
        server_default=sa.text("'PROCESSING'::statustype"),
    )

    op.alter_column(
        "documents",
        "imported_at",
        server_default=sa.text("CURRENT_DATE"),
    )


def downgrade() -> None:
    op.alter_column(
        "documents",
        "processing_status",
        server_default=sa.text("'FAILED'::statustype"),
    )

    op.alter_column(
        "documents",
        "imported_at",
        server_default=None,
    )
