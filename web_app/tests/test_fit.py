import hashlib
import pandas
import pickle
from sklearn.tree import DecisionTreeRegressor
from io import StringIO
from unittest import mock
from src.database import Model


def test_post_fit_valid_dataset(test_client, database):
    data = "age;sex;y\n0.0380759064334241;0.0506801187398187;151.0"
    response = test_client.post(
        "/dataset", files={"dataset": ("data.csv", StringIO(data), "text/csv")}
    )
    response.raise_for_status()
    dataset_id = response.json()["id"]

    response = test_client.post(f"/fit/{dataset_id}")
    response.raise_for_status()
    assert response.json() == {"id": mock.ANY}
    db_rows = database.query(Model).all()
    assert len(db_rows) == 1
    assert db_rows[0].id == response.json()["id"]

    df = pandas.read_csv(StringIO(data), sep=";")
    X = df.drop("y", axis=1)
    y = df["y"]
    expected_model = DecisionTreeRegressor(max_depth=2)
    expected_model.fit(X, y)
    assert db_rows[0].data == pickle.dumps(expected_model)
    assert db_rows[0].dataset_id == dataset_id
    assert db_rows[0].md5_hash == hashlib.md5(pickle.dumps(expected_model)).hexdigest()


def test_post_fit_same_dataset_twice(test_client, database):
    data = "age;sex;y\n0.0380759064334241;0.0506801187398187;151.0"
    response = test_client.post(
        "/dataset", files={"dataset": ("data.csv", StringIO(data), "text/csv")}
    )
    response.raise_for_status()
    dataset_id = response.json()["id"]

    response = test_client.post(f"/fit/{dataset_id}")
    response.raise_for_status()
    model_id = response.json()["id"]

    response = test_client.post(f"/fit/{dataset_id}")
    response.raise_for_status()
    assert response.json()["id"] == model_id

    db_rows = database.query(Model).all()
    assert len(db_rows) == 1

    df = pandas.read_csv(StringIO(data), sep=";")
    X = df.drop("y", axis=1)
    y = df["y"]
    expected_model = DecisionTreeRegressor(max_depth=2)
    expected_model.fit(X, y)
    assert db_rows[0].id == response.json()["id"]
    assert db_rows[0].data == pickle.dumps(expected_model)
    assert db_rows[0].dataset_id == dataset_id
    assert db_rows[0].md5_hash == hashlib.md5(pickle.dumps(expected_model)).hexdigest()


def test_post_fit_nonexisting_dataset(test_client, database):
    invalid_dataset_id = 123
    response = test_client.post(f"/fit/{invalid_dataset_id}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Dataset not found"}
