from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, drop_database, create_database
# import pymysql
from app.models.base import *
import models.base
from tabulate import tabulate

def load_all(session,name):
    tab = session.execute(text(f"Select * from {name}")).mappings().all()
    # print(tab)
    # cols = session.execute()
    print(tabulate(tab,headers="keys",tablefmt = "psql"))



# if __name__ == "__main__":
#     engine = create_engine(
#
#         connect_args={"charset": "utf8mb4"},
#         pool_pre_ping=True,
#         echo=False
#     )
#
#     # Управление базой данных
#     if not database_exists(engine.url):
#         create_database(engine.url)
#     else:
#         drop_database(engine.url)
#         create_database(engine.url)
#
#     # Создание таблиц
#     Base.metadata.create_all(engine)
#
#     # Создание сессии и заполнение данных
#     Session = sessionmaker(engine)
#     with Session(autoflush=True) as session:
#         # full_table(session)
#         boy1 = Boys(boy_name = "Alex", boy_age = 15, marks = 85)
#         print(load_all(session,"boys"))
#         print(boy1)