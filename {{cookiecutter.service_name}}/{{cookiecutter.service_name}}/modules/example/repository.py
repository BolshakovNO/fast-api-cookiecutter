from datetime import datetime, timedelta
from typing import Iterable, Optional

from sqlalchemy import desc, asc, func, text, true, null, and_, false, or_
from sqlalchemy.sql.expression import select, label, column, alias, insert, update
from sqlalchemy.sql.functions import count, func

from {{cookiecutter.service_name}}.common.exceptions import NotFound
from {{cookiecutter.service_name}}.common.models import OnlyId
from {{cookiecutter.service_name}}.modules.example.tables import (
    ExampleChildTable, ExampleTable
)
from {{cookiecutter.service_name}}.modules.example.models import (
    CreateExample, ExampleParent, Example, ExampleWithChild
)
from {{cookiecutter.service_name}}.common.repository import BaseRepository


class ExampleRepository(BaseRepository):

    async def create_example(self, example: CreateExample) -> int:
        example_parent = await self.save(ExampleTable(
            value=example.value
        ))
        for i in example.children:
            await self.save(ExampleChildTable(
                parent_id=example_parent.id,
                value=i
            ))
        return example_parent.id

    async def get_example_with_children(self, id: int) -> list[ExampleWithChild]:
        stmt = (
            select(
                ExampleTable.value,
                ExampleChildTable.value.label('child_value'),
            )
            .select_from(ExampleTable)
            .join(
                ExampleChildTable, ExampleChildTable.parent_id == ExampleTable.id
            )
            .where(and_(
                ExampleTable.id == id,
            ))
        )

        result = await self.execute(stmt)

        return [
            ExampleWithChild(
                value=item.value,
                child_value=item.child_value,
            )
            for item in result
        ]

    async def get_example(self, id: int) -> ExampleParent:
        stmt = (
            select(
                ExampleTable.value,
            )
            .where(and_(
                ExampleTable.id == id,
            ))
        )

        result = (await self.execute(stmt)).fetchone()

        if not result:
            raise NotFound()

        return ExampleParent(
            value=result.value
        )
