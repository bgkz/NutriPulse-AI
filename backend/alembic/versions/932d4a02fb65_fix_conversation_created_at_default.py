"""fix conversation created_at default

Revision ID: 932d4a02fb65
Revises: 65d735a0f6a5
Create Date: 2026-09-18 17:14:20.154706

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "932d4a02fb65"
down_revision: Union[str, Sequence[str], None] = "65d735a0f6a5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "conversations",
        "created_at",
        server_default=sa.text("now()"),
    )


def downgrade() -> None:
    op.alter_column(
        "conversations",
        "created_at",
        server_default=sa.text("CURRENT_DATE"),
    )
