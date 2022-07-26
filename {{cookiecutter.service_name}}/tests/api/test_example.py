import pytest

from fastapi.testclient import TestClient


def test_create_example(client: TestClient, example_create_data_1):
    response = client.post("/example", json=example_create_data_1)
    assert response.status_code == 200, response.text
    model = response.json()

    response = client.get(f"/example/{model['id']}/children")

    assert response.status_code == 200, response.text
    data = response.json()

    assert data == example_create_data_1


@pytest.mark.usefixtures('example_mock_func_1')
def test_get_example_list(client: TestClient, example_create_data_2):
    response = client.get(f"/example/123/children")
    assert response.status_code == 200, response.text
    data = response.json()

    assert data == example_create_data_2


def test_get_example(client: TestClient, example_model_1):
    response = client.get(f"/example/{example_model_1.id}")
    assert response.status_code == 200, response.text
    data = response.json()

    assert data['value'] == example_model_1.value
