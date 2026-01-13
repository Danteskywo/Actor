"""Initial migration

Revision ID: 6f39fdb1e26f
Revises: 2970b6e65688
Create Date: 2026-01-12 21:03:31.899629

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6f39fdb1e26f'
down_revision: Union[str, Sequence[str], None] = '2970b6e65688'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
