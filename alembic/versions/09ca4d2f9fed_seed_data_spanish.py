"""seed_data_spanish

Revision ID: 09ca4d2f9fed
Revises: 2fb1dd1fd88a
Create Date: 2025-12-30 15:11:15.438920

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '09ca4d2f9fed'
down_revision: Union[str, Sequence[str], None] = '2fb1dd1fd88a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
