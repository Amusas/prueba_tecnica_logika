"""add_user_id_to_tasks

Revision ID: 2fb1dd1fd88a
Revises: a172110a5699
Create Date: 2025-12-30 14:49:55.021505

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2fb1dd1fd88a'
down_revision: Union[str, Sequence[str], None] = 'a172110a5699'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # 1. Add column as nullable first
    op.add_column('tasks', sa.Column('user_id', sa.Integer(), nullable=True))
    
    # 2. Update existing rows to have a user_id (e.g., 1)
    op.execute("UPDATE tasks SET user_id = 1 WHERE user_id IS NULL")
    
    # 3. Alter column to be NOT NULL
    op.alter_column('tasks', 'user_id', nullable=False)
    
    op.create_index(op.f('ix_tasks_user_id'), 'tasks', ['user_id'], unique=False)
    op.create_foreign_key(None, 'tasks', 'users', ['user_id'], ['id'])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, 'tasks', type_='foreignkey')
    op.drop_index(op.f('ix_tasks_user_id'), table_name='tasks')
    op.drop_column('tasks', 'user_id')
