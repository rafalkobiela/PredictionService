import hashlib
from io import StringIO
from unittest import mock
from src.database import Dataset


def test_post_dataset_valid_file(test_client, database):
    data = "age;sex;y\n0.0380759064334241;0.0506801187398187;151.0"
    response = test_client.post(
        "/dataset", files={"dataset": ("data.csv", StringIO(data), "text/csv")}
    )
    response.raise_for_status()

    assert response.json() == {"id": mock.ANY}
    db_rows = database.query(Dataset).all()
    assert len(db_rows) == 1
    assert db_rows[0].id == response.json()["id"]
    assert db_rows[0].data == data.encode()
    assert db_rows[0].md5_hash == hashlib.md5(data.encode()).hexdigest()


def test_post_dataset_same_file_twice(test_client, database):
    data = "age;sex;y\n0.0380759064334241;0.0506801187398187;151.0"
    response = test_client.post(
        "/dataset", files={"dataset": ("data.csv", StringIO(data), "text/csv")}
    )
    response.raise_for_status()
    dataset_id = response.json()["id"]

    response = test_client.post(
        "/dataset", files={"dataset": ("data.csv", StringIO(data), "text/csv")}
    )
    response.raise_for_status()
    assert response.json()["id"] == dataset_id
    db_rows = database.query(Dataset).all()
    assert len(db_rows) == 1
    assert db_rows[0].id == response.json()["id"]
    assert db_rows[0].data == data.encode()
    assert db_rows[0].md5_hash == hashlib.md5(data.encode()).hexdigest()


def test_post_dataset_empty_file(test_client):
    data = StringIO("")
    response = test_client.post(
        "/dataset", files={"dataset": ("data.csv", data, "text/csv")}
    )
    assert response.status_code == 422
    assert response.json() == {"detail": "Input file is empty"}


def test_post_dataset_missing_X(test_client):
    data = StringIO("y\n151.0")
    response = test_client.post(
        "/dataset", files={"dataset": ("data.csv", data, "text/csv")}
    )
    assert response.status_code == 422
    assert response.json() == {"detail": "X is missing"}


def test_post_dataset_missing_y(test_client):
    data = StringIO("age;sex\n0.0380759064334241;0.0506801187398187")
    response = test_client.post(
        "/dataset", files={"dataset": ("data.csv", data, "text/csv")}
    )
    assert response.status_code == 422
    assert response.json() == {"detail": "y is missing"}
