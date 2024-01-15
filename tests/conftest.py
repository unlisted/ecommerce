import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy_utils import create_database, database_exists, drop_database
from ecommerce.common.db import Base
import os

os.environ["POSTGRES_HOST"] = "localhost"
DATABASE_URL = f"postgresql+psycopg2://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@{os.getenv("POSTGRES_HOST")}:5432/{os.getenv("POSTGRES_DB")}_test"


@pytest.fixture(autouse=True, scope="session")   
def engine():
    engine = create_engine(DATABASE_URL, echo=True)
    yield engine

    print("Disposing engine")
    engine.dispose()


@pytest.fixture(autouse=True, scope="session")
def create_db(engine):
    if not database_exists(DATABASE_URL):
        create_database(engine.url)
        print("Database created")
    yield
    if database_exists(DATABASE_URL):
        drop_database(engine.url)
        print("Database dropped")


@pytest.fixture(autouse=True)
def create_tables(engine):
    Base.metadata.create_all(engine)


@pytest.fixture(autouse=True)
def db_session(engine):
    yield Session(engine)

