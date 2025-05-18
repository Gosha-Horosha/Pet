from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Пример URL подключения (замените на ваш)
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/dbname"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def current_session():
    current_session = Session()
    try:
        yield current_session
    finally:
        current_session.close()