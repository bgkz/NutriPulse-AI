"""update conversation created_at

Revision ID: 65d735a0f6a5
Revises: f03638f76152
Create Date: 2026-09-18 17:12:57.203183

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "65d735a0f6a5"
down_revision: Union[str, Sequence[str], None] = "f03638f76152"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint(
        op.f("conversations_title_key"),
        "conversations",
        type_="unique",
    )

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

    op.create_unique_constraint(
        op.f("conversations_title_key"),
        "conversations",
        ["title"],
        postgresql_nulls_not_distinct=False,
    )
