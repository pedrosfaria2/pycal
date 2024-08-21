import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import get_db, Base
from alembic.config import Config
from alembic import command
import logging
from io import StringIO

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://user:password@localhost/"
TEMP_DB_NAME = "test_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    with engine.connect() as connection:
        connection.execute(text(f"DROP DATABASE IF EXISTS {TEMP_DB_NAME}"))
        connection.execute(text(f"CREATE DATABASE {TEMP_DB_NAME}"))
        connection.execute(text(f"USE {TEMP_DB_NAME}"))

    test_engine = create_engine(f"mysql+pymysql://user:password@localhost/{TEMP_DB_NAME}")
    TestingSessionLocal.configure(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", f"mysql+pymysql://user:password@localhost/{TEMP_DB_NAME}")
    command.upgrade(alembic_cfg, "head")

    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=test_engine)
        with engine.connect() as connection:
            connection.execute(text(f"DROP DATABASE IF EXISTS {TEMP_DB_NAME}"))


@pytest.fixture(scope="function")
def client(db_session):
    def _get_db_override():
        yield db_session

    app.dependency_overrides[get_db] = _get_db_override
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def logger():
    log_stream = StringIO()
    handler = logging.StreamHandler(log_stream)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    yield log_stream

    logger.removeHandler(handler)
