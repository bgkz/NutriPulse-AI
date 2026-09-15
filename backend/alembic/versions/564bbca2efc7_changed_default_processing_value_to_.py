"""changed default processing value to PROCESSING instead of FAILED

Revision ID: 564bbca2efc7
Revises: 2c215cef6798
Create Date: 2026-09-15 21:58:46.182944

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "564bbca2efc7"
down_revision: Union[str, Sequence[str], None] = "2c215cef6798"
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
