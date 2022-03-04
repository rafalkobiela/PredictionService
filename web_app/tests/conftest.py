import pytest
from src.main import app
from src.database import get_db, Dataset, Model
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError


@pytest.fixture
def test_client():
    return TestClient(app)


@pytest.fixture(scope="session")
def database():
    db = next(get_db())
    yield db


@pytest.fixture(autouse=True)
def clean_database(database):
    def clean():
        try:
            database.query(Model).delete()
            database.query(Dataset).delete()
            database.commit()
        except SQLAlchemyError:
            database.rollback()
            raise

    clean()
    yield
    clean()
