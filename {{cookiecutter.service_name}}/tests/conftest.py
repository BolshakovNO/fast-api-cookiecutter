import asyncio
from typing import Generator

import pytest
from fastapi.testclient import TestClient

from {{cookiecutter.service_name}}.main import app
from {{cookiecutter.service_name}}.common.db import Database


pytest_plugins = [
    "{{cookiecutter.service_name}}.modules.fixtures.access",
]


@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def client() -> Generator:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="session")
def config() -> dict:
    return app.container.config()


@pytest.fixture(scope="session")
def db(config) -> Database:
    db = Database(config['gateways']['db']['url'])
    yield db


@pytest.fixture(scope="session")
def user_id_1():
    return 1


@pytest.fixture(scope="session")
def username_1():
    return 'user1'


@pytest.fixture(scope="session")
def battle_id_1():
    return 2
