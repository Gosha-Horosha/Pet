"""pairs

Revision ID: 97c788596f4a
Revises: 280db7ad76f5
Create Date: 2025-05-18 20:04:23.010742

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '97c788596f4a'
down_revision: Union[str, None] = '280db7ad76f5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'pair_reviews',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('boy_id', sa.Integer),
        sa.Column('girl_id', sa.Integer),
        sa.Column('review', sa.String(200)),
        sa.ForeignKeyConstraint(
            ['boy_id', 'girl_id'],
            ['boys_girls.boy_id', 'boys_girls.girl_id'],
            ondelete='RESTRICT'
        )
    )

def downgrade():
    op.drop_table('pair_reviews')
