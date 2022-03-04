from io import StringIO


def test_get_predict_valid_model(test_client, database):
    data = "age;sex;y\n0.0380759064334241;0.0506801187398187;151.0"
    response = test_client.post(
        "/dataset", files={"dataset": ("data.csv", StringIO(data), "text/csv")}
    )
    response.raise_for_status()
    dataset_id = response.json()["id"]

    response = test_client.post(f"/fit/{dataset_id}")
    response.raise_for_status()
    model_id = response.json()["id"]

    input_data = "age;sex\n0.0380759064334241;0.0506801187398187"
    response = test_client.get(
        f"/predict/{model_id}",
        files={"input_data": ("data.csv", StringIO(input_data), "text/csv")},
    )
    response.raise_for_status()
    assert response.json() == [151.0]


def test_get_predict_nonexisting_model(test_client, database):
    invalid_model_id = 123
    input_data = "age;sex\n0.0380759064334241;0.0506801187398187"
    response = test_client.get(
        f"/predict/{invalid_model_id}",
        files={"input_data": ("data.csv", StringIO(input_data), "text/csv")},
    )
    assert response.status_code == 404
