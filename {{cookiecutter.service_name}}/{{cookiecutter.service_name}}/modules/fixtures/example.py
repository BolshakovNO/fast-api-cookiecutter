from pathlib import Path

import pytest
import pytest_asyncio

from {{cookiecutter.service_name}}.main import app
from {{cookiecutter.service_name}}.common.db import Database
from {{cookiecutter.service_name}}.modules.access.tables import BattleSmtpTable
from {{cookiecutter.service_name}}.modules.external.fishing_smtp import FishingSmtpClient


@pytest.fixture
def example_value_1():
    return '6d82b724a6b94e9cb3d68da3cd9211e4'


@pytest_asyncio.fixture(scope="function")
async def example_model_1(db: Database, battle_id_1):
    model = await db.get_or_create(BattleSmtpTable(
        battle_id=battle_id_1,
        webapp_address='mail.services.stf',
        smtp_domain='services.stf',
        ssh_key='key',
        ssh_user='autoadd',
        ssh_address='localhost'
    ))
    yield model
    await db.delete(model)


@pytest.fixture
def example_mock_func_1(monkeypatch):
    async def smtp_mock(*args, **kwargs):
        return FishingSmtpClient.build_email(kwargs['login'], kwargs['smtp_domain'])

    monkeypatch.setattr(FishingSmtpClient, 'create_fishing_smtp_user', smtp_mock)
