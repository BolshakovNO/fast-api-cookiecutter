import pytest

from fastapi.testclient import TestClient

from {{cookiecutter.service_name}}.modules.access.service import AccessService


def test_access_get_vpn(client: TestClient, user_id_1, battle_smtp):
    response = client.get("/access/vpn_config", params={'user_id': user_id_1})
    assert response.status_code == 200, response.text
    data = response.content.decode()

    assert 'BEGIN CERTIFICATE' in data


@pytest.mark.usefixtures('mock_smtp_create')
def test_get_smtp_account_for_fishing(client: TestClient, battle_id_1, user_id_1, username_1, battle_smtp):
    response = client.post(f"/access/cyberbattle/{battle_id_1}/email_account", json={
        'user_id': user_id_1,
        'username': username_1
    })
    assert response.status_code == 200, response.text
    data = response.json()

    assert data.pop('password')

    login = AccessService.generate_login(username_1, user_id_1)

    assert data == {
        'url': 'mail.services.stf',
        'login': f'{login}@services.stf',
    }


@pytest.mark.usefixtures('mock_encryptor_getter')
def test_get_encryptor(client: TestClient, battle_id_1, encryptor_1):
    response = client.get(f"/access/cyberbattle/{battle_id_1}/encryptor")
    assert response.status_code == 200, response.text
    data = response.content

    assert data == encryptor_1
