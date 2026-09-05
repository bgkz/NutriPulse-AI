"""remove nutrition and exercise sets

Revision ID: 4838d9c518af
Revises: ab22fcc9a274
Create Date: 2026-09-05 22:48:38.839731

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "4838d9c518af"
down_revision: Union[str, Sequence[str], None] = "ab22fcc9a274"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_table("exercise_sets")
    op.drop_table("nutritions")


def downgrade() -> None:
    # optional: Tabellen hier wiederherstellen
    pass
