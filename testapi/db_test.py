import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, NullPool
from sqlalchemy.orm import sessionmaker
from config import DB_USER_TEST, DB_NAME_TEST, DB_PORT_TEST, DB_HOST_TEST, DB_PASS_TEST
from main import app
from scr.database.db import Session_factory
from scr.database.models import Base


DB_TEST = f"postgresql+psycopg2://{DB_USER_TEST}:{DB_PASS_TEST}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}"

engine_test = create_engine(DB_TEST, poolclass=NullPool, echo=False)
session_maker_Test = sessionmaker(engine_test)

base_obj = Base.metadata
base_obj.bind = engine_test


def override_get_session():
    with session_maker_Test() as session:
        yield session


app.dependency_overrides[Session_factory] = override_get_session


@pytest.fixture(autouse=True, scope='function')
def function_scoped_session():
    session = session_maker_Test()
    yield session
    session.rollback()
    session.close()


@pytest.fixture(autouse=True, scope='session')
def prepare_database():
    base_obj.create_all(engine_test)
    yield
    base_obj.drop_all(engine_test)


client = TestClient(app)
