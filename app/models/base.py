from typing import List, Optional, Annotated

from sqlalchemy import Select, Column, Integer, String, ForeignKey, Table, insert, select, exists, ForeignKeyConstraint, \
    and_, Boolean, Engine, text, update, func, Null
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, validates, Session, MappedAsDataclass, \
    selectinload, joinedload, raiseload, subqueryload


name = Annotated[str, mapped_column(String(25))],
small_int = Annotated[int, mapped_column(TINYINT(unsigned=True))]



class Base(MappedAsDataclass, DeclarativeBase):
    type_annotation_map = {
        small_int: TINYINT(unsigned=True),
        name: String(25)
        }


boys_girls = Table(
    "boys_girls",
    Base.metadata,
    Column("boy_id", ForeignKey("boys.boy_id",ondelete="cascade"), primary_key=True),
    Column("girl_id", ForeignKey("girls.girl_id",ondelete="cascade"), primary_key=True),
)


class Boys(Base):
    __tablename__ = "boys"

    boy_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True,init=False)
    boy_name: Mapped[name]
    boy_age: Mapped[small_int]
    marks: Mapped[small_int]

    # girls: Mapped[List["Girls"]] = relationship(
    #     secondary=boys_girls,
    #     back_populates="boys",
    #     repr=False
    # )

    girls: Mapped[Optional[List["Girls"]]] = relationship(
        secondary=boys_girls,
        # lazy="write_only",
        viewonly=False, # Разрешаем изменения
        repr=True,
        # default_factory=list
    )

    conscription: Mapped[Optional["Conscription"]] = relationship(
        "Conscription",
        back_populates="boy",
        uselist=False,
        # default= None,
        single_parent=True # Логично в родительском классе
    )

    @validates("marks")
    def validate_mark(self, key, value):
        if not 0 <= value <= 100:
            raise ValueError("Marks must be between 0 and 100")
        return value


class Girls(Base):
    __tablename__ = "girls"

    girl_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True,init=False)
    girl_name: Mapped[name]
    girl_age: Mapped[small_int]
    marks: Mapped[small_int]

    boys: Mapped[List["Boys"]] = relationship(
        secondary=boys_girls,
        back_populates="girls",
        repr=False,
        default_factory=list
        # passive_deletes=True
    )


class PairReview(Base):
    __tablename__ = "pair_reviews"

    id: Mapped[int] = mapped_column(Integer, primary_key=True,autoincrement=True,init=False)
    boy_id: Mapped[int] = mapped_column(Integer)
    girl_id: Mapped[int] = mapped_column(Integer)
    review: Mapped[str] = mapped_column(String(200))

    __table_args__ = (
        ForeignKeyConstraint(
            ["boy_id", "girl_id"],
            ["boys_girls.boy_id", "boys_girls.girl_id"],
            ondelete="Restrict"
        ),
    )

class Conscription(Base):
    __tablename__ = "conscription"

    conscription_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True,init=False)
    is_fit: Mapped[bool] = mapped_column(Boolean, nullable=False)
    reason: Mapped[Optional[str]] = mapped_column(String(100))

    #1.5.1 Set Null
    boy_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey
            (
            "boys.boy_id",
            # ondelete="Set Null"
            # ondelete = "CASCADE"
        ),
        unique=True,
        nullable=False)



    boy: Mapped["Boys"] = relationship(
        "Boys",
        back_populates="conscription",
        repr=False,
        init = False
    )



def full_table(session: Session) -> None:
    # Вставка данных в boys
    boys_data = [
        {"boy_name": "Alex", "boy_age": 15, "marks": 85},
        {"boy_name": "Max", "boy_age": 16, "marks": 90},
        {"boy_name": "John", "boy_age": 14, "marks": 78}
    ]
    session.execute(insert(Boys), boys_data)

    # Вставка данных в girls
    girls_data = [
        {"girl_name": "Anna", "girl_age": 15, "marks": 92},
        {"girl_name": "Lisa", "girl_age": 16, "marks": 88},
        {"girl_name": "Emma", "girl_age": 14, "marks": 95}
    ]
    session.execute(insert(Girls), girls_data)
    session.commit()
    # Создание связей между мальчиками и девочками
    session.execute(
        insert(boys_girls),
        [
            {"boy_id": 1, "girl_id": 1},  # Alex - Anna
            {"boy_id": 1, "girl_id": 2},  # Alex - Lisa
            {"boy_id": 3, "girl_id": 3},  # John - Emma
        ]
    )

    reviews = [
        PairReview(
            boy_id=1,
            girl_id=1,
            review="SomebodyU_loved"
        ),
        PairReview(
            boy_id=1,
            girl_id=2,
            review = "friendsWithBenefits"
        ),
        PairReview(
            boy_id=3,
            girl_id=3,
            review="Kink"
        )
    ]
    # session.flush()
    # print(session.new)
    # for x in reviews:
    #     session.add(x)
    #     session.flush()
    session.add_all(reviews)


    session.commit()

