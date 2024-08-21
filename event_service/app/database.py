from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "mysql+pymysql://user:password@localhost/dbname"
BASE_DATABASE_URL = "mysql+pymysql://user:password@localhost"


def create_database_if_not_exists():
    temp_engine = create_engine(BASE_DATABASE_URL)

    with temp_engine.connect() as connection:
        connection.execute(text("CREATE DATABASE IF NOT EXISTS `dbname`"))


#        print("Banco de dados criado com sucesso ou já existe.")


create_database_if_not_exists()

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
