from datetime import datetime, timedelta
from typing import Iterable, Optional

from sqlalchemy import desc, asc, func, text, true, null, and_, false, or_
from sqlalchemy.sql.expression import select, label, column, alias, insert, update
from sqlalchemy.sql.functions import count, func

from {{cookiecutter.service_name}}.common.exceptions import NotFound
from {{cookiecutter.service_name}}.common.models import OnlyId
from {{cookiecutter.service_name}}.modules.{{cookiecutter.module_name}}.tables import (
    {{cookiecutter.module_name | capitalize}}Table,
)
from {{cookiecutter.service_name}}.modules.{{cookiecutter.module_name}}.models import (
    {{cookiecutter.module_name | capitalize}}
)
from {{cookiecutter.service_name}}.common.repository import BaseRepository


class {{cookiecutter.module_name | capitalize}}Repository(BaseRepository):

    async def create_{{cookiecutter.module_name}}(self, {{cookiecutter.module_name}}: {{cookiecutter.module_name | capitalize}}) -> int:
        {{cookiecutter.module_name}}_parent = await self.save({{cookiecutter.module_name | capitalize}}Table(
            value={{cookiecutter.module_name}}.value
        ))
        return {{cookiecutter.module_name}}_parent.id
