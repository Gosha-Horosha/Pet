"""Create tables

Revision ID: 745df9be5755
Revises: 
Create Date: 2025-05-18 19:46:07.634970

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '745df9be5755'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'boys',
        sa.Column('boy_id', sa.Integer, primary_key=True),
        sa.Column('boy_name', sa.String(25)),
        sa.Column('boy_age', sa.Integer),
        sa.Column('marks', sa.Integer)
    )

def downgrade():
    op.drop_table('boys')