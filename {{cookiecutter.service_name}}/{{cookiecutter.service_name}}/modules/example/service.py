import ipaddress
from fastapi.logger import logger
from datetime import datetime, timedelta
from typing import Iterable, TYPE_CHECKING

from {{cookiecutter.service_name}}.common.exceptions import NotFound
from {{cookiecutter.service_name}}.common.models import OnlyId
from {{cookiecutter.service_name}}.modules.example.repository import ExampleRepository
from {{cookiecutter.service_name}}.modules.example.models import (
    Example, ExampleWithChild, ExampleParent, CreateExample
)

if TYPE_CHECKING:
    from {{cookiecutter.service_name}}.container import Repositories
    from {{cookiecutter.service_name}}.container import Gateways


class ExampleService:
    def __init__(
        self,
        repositories: 'Repositories',
        gateways: 'Gateways',
    ) -> None:
        self._example_repo: ExampleRepository = repositories.example()

    async def create_example(self, example_request: CreateExample) -> OnlyId:
        id = await self._example_repo.create_example(example_request)
        return OnlyId(
            id=id
        )

    async def get_example_with_children(self, id: int) -> Example:
        result = await self._example_repo.get_example_with_children(id=id)

        parent_value = result[0].value
        children = [
            item.child_value
            for item in result
        ]
        return Example(
            value=parent_value,
            children=children
        )

    async def get_example(self, id: int) -> ExampleParent:
        return await self._example_repo.get_example(id=id)
