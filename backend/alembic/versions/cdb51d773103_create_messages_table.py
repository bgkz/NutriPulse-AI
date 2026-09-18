"""create messages table

Revision ID: cdb51d773103
Revises: 932d4a02fb65
Create Date: 2026-09-18 18:41:06.990541

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cdb51d773103'
down_revision: Union[str, Sequence[str], None] = '932d4a02fb65'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
