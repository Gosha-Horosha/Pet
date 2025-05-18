"""full tables

Revision ID: a1f0579b8694
Revises: aa7ce5e2a3b1
Create Date: 2025-05-18 20:06:40.137604

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import table
from sqlalchemy.orm import Session

from app.models import Boys,Girls
from app.models.base import Conscription,PairReview

# revision identifiers, used by Alembic.
revision: str = 'a1f0579b8694'
down_revision: Union[str, None] = 'aa7ce5e2a3b1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Создаем сессию через существующее соединение
    bind = op.get_bind()
    session = Session(bind=bind)

    try:
        boys = [
            Boys(boy_name="Alex", boy_age=15, marks=85),
            Boys(boy_name="Max", boy_age=16, marks=90),
            Boys(boy_name="John", boy_age=14, marks=78)
        ]
        session.add_all(boys)

        girls = [
            Girls(girl_name="Anna", girl_age=15, marks=92),
            Girls(girl_name="Lisa", girl_age=16, marks=88),
            Girls(girl_name="Emma", girl_age=14, marks=95)
        ]
        session.add_all(girls)

        session.flush() # айдишнки во флаше

        boys[0].girls = [girls[0], girls[1]]
        boys[2].girls = [girls[2]]

        # session.flush() # айдишнки во флаше
        session.commit()

    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def downgrade():
    bind = op.get_bind()
    session = Session(bind=bind)

    try:
        # Удаляем в порядке, обратном зависимостям
        # session.query(Conscription).delete()
        # session.query(PairReview).delete()

        # Для many-to-many сначала очищаем таблицу связей
        for boy in session.query(Boys).all():
            boy.girls = []

        session.query(Girls).delete()
        session.query(Boys).delete()
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()