import pytest
import pytest_asyncio

from {{cookiecutter.service_name}}.common.db import Database
from {{cookiecutter.service_name}}.modules.example.tables import ExampleTable
from {{cookiecutter.service_name}}.modules.example.service import ExampleService
from {{cookiecutter.service_name}}.modules.example.models import Example


@pytest.fixture
def example_value_1():
    return '6d82b724a6b94e9cb3d68da3cd9211e4'


@pytest.fixture
def example_create_data_1():
    return {
        'value': 'test-1',
        'children': ['child-test-1']
    }


@pytest.fixture
def example_create_data_2():
    return {
        'value': 'test-2',
        'children': ['child-test-2']
    }


@pytest_asyncio.fixture(scope="function")
async def example_model_1(db: Database, example_value_1) -> ExampleTable:
    model = await db.get_or_create(ExampleTable(
        value=example_value_1,
    ))
    yield model
    await db.delete(model)


@pytest.fixture
def example_mock_func_1(monkeypatch, example_create_data_2):
    async def example_mock(*args, **kwargs):
        return Example(**example_create_data_2)

    monkeypatch.setattr(ExampleService, 'get_example_with_children', example_mock)
