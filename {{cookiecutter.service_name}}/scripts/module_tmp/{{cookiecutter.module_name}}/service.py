import ipaddress
from fastapi.logger import logger
from datetime import datetime, timedelta
from typing import Iterable, TYPE_CHECKING

from {{cookiecutter.service_name}}.common.exceptions import NotFound
from {{cookiecutter.service_name}}.common.models import OnlyId
from {{cookiecutter.service_name}}.modules.{{cookiecutter.module_name}}.repository import {{cookiecutter.module_name | capitalize}}Repository
from {{cookiecutter.service_name}}.modules.{{cookiecutter.module_name}}.models import (
    {{cookiecutter.module_name | capitalize}}
)

if TYPE_CHECKING:
    from {{cookiecutter.service_name}}.container import Repositories
    from {{cookiecutter.service_name}}.container import Gateways


class {{cookiecutter.module_name | capitalize}}Service:
    def __init__(
        self,
        repositories: 'Repositories',
        gateways: 'Gateways',
    ) -> None:
        self._{{cookiecutter.module_name}}_repo: {{cookiecutter.module_name | capitalize}}Repository = repositories.{{cookiecutter.module_name}}()

    async def create_{{cookiecutter.module_name}}(self, {{cookiecutter.module_name}}_request: {{cookiecutter.module_name | capitalize}}) -> OnlyId:
        id = await self._{{cookiecutter.module_name}}_repo.create_{{cookiecutter.module_name}}({{cookiecutter.module_name}}_request)
        return OnlyId(
            id=id
        )
