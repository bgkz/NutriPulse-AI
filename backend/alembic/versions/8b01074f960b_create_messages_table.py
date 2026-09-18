"""create messages table

Revision ID: 8b01074f960b
Revises: cdb51d773103
Create Date: 2026-09-18 18:41:34.538428

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8b01074f960b'
down_revision: Union[str, Sequence[str], None] = 'cdb51d773103'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
