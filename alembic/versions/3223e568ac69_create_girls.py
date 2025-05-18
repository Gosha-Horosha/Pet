"""Create Girls

Revision ID: 3223e568ac69
Revises: 745df9be5755
Create Date: 2025-05-18 19:57:56.756995

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3223e568ac69'
down_revision: Union[str, None] = '745df9be5755'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    op.create_table(
        'girls',
        sa.Column('girl_id', sa.Integer, primary_key=True),
        sa.Column('girl_name', sa.String(25)),
        sa.Column('girl_age', sa.Integer),
        sa.Column('marks', sa.Integer)
    )

def downgrade():
    op.drop_table('girls')