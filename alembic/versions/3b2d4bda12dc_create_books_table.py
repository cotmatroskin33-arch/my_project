"""create books table

Revision ID: 3b2d4bda12dc
Revises: 0e3f256d364c
Create Date: 2026-07-29 14:40:38.865690

"""
from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '3b2d4bda12dc'
down_revision: str | Sequence[str] | None = '0e3f256d364c'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table('books',
                    sa.Column('id', sa.Uuid(), nullable=False),
                    sa.Column('title', sa.String(length=255), nullable=False),
                    sa.Column('author', sa.String(length=255), nullable=False),
                    sa.Column('description', sa.Text(), nullable=False),
                    sa.Column('price', sa.Integer(), nullable=False),
                    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'),
                              nullable=False),
                    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'),
                              nullable=False),
                    sa.Column('is_deleted', sa.Boolean(), server_default=sa.text('false'), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )

def downgrade() -> None:
    op.drop_table('books')
