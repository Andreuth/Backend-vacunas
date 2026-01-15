"""merge heads

Revision ID: 27c0589dca20
Revises: 765f6312d1e4, 845a9bfbbfa4
Create Date: 2026-01-15 00:31:00.736026

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '27c0589dca20'
down_revision: Union[str, Sequence[str], None] = ('765f6312d1e4', '845a9bfbbfa4')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
