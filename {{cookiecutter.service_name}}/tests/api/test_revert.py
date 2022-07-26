import pytest

from fastapi.testclient import TestClient


def test_create_revert_request(client: TestClient, battle_id_1, user_id_1, username_1, revert_vm_1):
    response = client.post(f"/revert/cyberbattle/{battle_id_1}", json={
        'user_id': user_id_1,
        'address': revert_vm_1.fqdn
    })
    assert response.status_code == 200, response.text
    data = response.json()

    assert isinstance(data['revertAt'], int)


def test_create_revert_not_found_request(client: TestClient, battle_id_1, user_id_1, username_1, revert_vm_1):
    response = client.post(f"/revert/cyberbattle/{battle_id_1}", json={
        'user_id': user_id_1,
        'address': 'asdf'
    })
    assert response.status_code == 404, response.text


def test_get_new_revert_requests(client: TestClient, user_id_1, battle_id_1, revert_vm_1, revert_request_1):  # nosec
    response = client.get(f"/revert/cyberbattle/{battle_id_1}/new")
    assert response.status_code == 200, response.text
    data = response.json()

    assert data == [{'name': revert_vm_1.fqdn}]


def test_get_status_not_revert_requests(client: TestClient, user_id_1, battle_id_1, revert_vm_1, revert_request_1):  # nosec
    response = client.post(f"/revert/cyberbattle/{battle_id_1}/status", json=[{
        'name': revert_vm_1.fqdn,
        'reverted': False
    }])
    assert response.status_code == 200, response.text

    response = client.get(f"/revert/cyberbattle/{battle_id_1}/new")
    assert response.status_code == 200, response.text
    data = response.json()

    assert data == [{'name': revert_vm_1.fqdn}]


def test_get_status_revert_requests(client: TestClient, user_id_1, battle_id_1, revert_vm_1, revert_request_1):  # nosec
    response = client.post(f"/revert/cyberbattle/{battle_id_1}/status", json=[{
        'name': revert_vm_1.fqdn,
        'reverted': True
    }])
    assert response.status_code == 200, response.text

    response = client.get(f"/revert/cyberbattle/{battle_id_1}/new")
    assert response.status_code == 200, response.text
    data = response.json()

    assert not data
