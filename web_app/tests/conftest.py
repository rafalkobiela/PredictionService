import pytest


@pytest.fixture
def test_client():
    from src.main import app
    from fastapi.testclient import TestClient

    return TestClient(app)


@pytest.fixture(scope="session")
def database():
    from src.database import get_db

    db = next(get_db())
    yield db
