"""conscription

Revision ID: aa7ce5e2a3b1
Revises: 97c788596f4a
Create Date: 2025-05-18 20:04:38.089208

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aa7ce5e2a3b1'
down_revision: Union[str, None] = '97c788596f4a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'conscription',
        sa.Column('conscription_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('is_fit', sa.Boolean, nullable=False),
        sa.Column('reason', sa.String(100), nullable=True),
        sa.Column('boy_id', sa.Integer, sa.ForeignKey('boys.boy_id', ondelete='SET NULL'), unique=True, nullable=True)
    )

def downgrade():
    op.drop_table('conscription')