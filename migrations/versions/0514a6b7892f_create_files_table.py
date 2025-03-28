"""create files table

Revision ID: 0514a6b7892f
Revises: c7451858a8fd
Create Date: 2025-03-29 03:47:52.285887

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0514a6b7892f'
down_revision: Union[str, None] = 'c7451858a8fd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'files',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('path', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=False),
        sa.Column('metadatas', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.create_index('ix_files_name', 'files', ['name'], unique=True)
    

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index('ix_files_name', table_name='files')
    op.drop_table('files')
