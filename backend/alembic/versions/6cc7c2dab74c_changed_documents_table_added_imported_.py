"""changed documents table, added imported_at column and processing (enum) column

Revision ID: 6cc7c2dab74c
Revises: b5cf56cbe81b
Create Date: 2026-09-15 21:53:34.874041

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "6cc7c2dab74c"
down_revision: Union[str, Sequence[str], None] = "b5cf56cbe81b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    status_type = sa.Enum("FAILED", "PROCESSING", "SUCCESS", name="statustype")

    # Enum zuerst in PostgreSQL erstellen
    status_type.create(op.get_bind(), checkfirst=True)

    op.add_column("documents", sa.Column("imported_at", sa.Date(), nullable=False))

    op.add_column(
        "documents",
        sa.Column(
            "processing_status", status_type, nullable=False, server_default="FAILED"
        ),
    )


def downgrade():
    op.drop_column("documents", "processing_status")
    op.drop_column("documents", "imported_at")

    status_type = sa.Enum("FAILED", "PROCESSING", "SUCCESS", name="statustype")

    status_type.drop(op.get_bind(), checkfirst=True)
