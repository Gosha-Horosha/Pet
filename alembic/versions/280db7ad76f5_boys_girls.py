"""boys_girls

Revision ID: 280db7ad76f5
Revises: 3223e568ac69
Create Date: 2025-05-18 20:01:32.327968

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '280db7ad76f5'
down_revision: Union[str, None] = '3223e568ac69'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    op.create_table(
        'boys_girls',
        sa.Column('boy_id', sa.Integer, sa.ForeignKey('boys.boy_id', ondelete='CASCADE'), primary_key=True),
        sa.Column('girl_id', sa.Integer, sa.ForeignKey('girls.girl_id', ondelete='CASCADE'), primary_key=True)
    )

def downgrade():
    op.drop_table('boys_girls')
