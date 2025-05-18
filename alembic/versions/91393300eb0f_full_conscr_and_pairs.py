"""full conscr and pairs

Revision ID: 91393300eb0f
Revises: a1f0579b8694
Create Date: 2025-05-18 21:37:50.241394

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import  Session

from app.models.base import PairReview, Conscription, Boys, Girls

# revision identifiers, used by Alembic.
revision: str = '91393300eb0f'
down_revision: Union[str, None] = 'a1f0579b8694'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    session = Session(bind=bind)
    # x = session.get(Boys,1)
    # y = session.get(Girls,1)
    # print(x,y)
    reviews = [
            PairReview(boy_id=1, girl_id=1, review="SomebodyU_loved"),
            PairReview(boy_id=1, girl_id=2, review="friendsWithBenefits"),
            PairReview(boy_id=3, girl_id=3, review="Kink")
        ]
    session.add_all(reviews)

    # session.commit()
    session.flush()

    conscriptions = [
        Conscription(boy_id=1, is_fit=True, reason="Абсолютно здоров"),
        Conscription(boy_id=2, is_fit=False, reason="Близорукость"),
        Conscription(boy_id=3, is_fit=True, reason="Годен без ограничений")
    ]
    session.add_all(conscriptions)
    session.flush()
    session.commit()


def downgrade() -> None:
    bind = op.get_bind()
    session = Session(bind=bind)
    try:
        # Удаляем в порядке, обратном зависимостям
        session.query(Conscription).delete()
        session.query(PairReview).delete()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()