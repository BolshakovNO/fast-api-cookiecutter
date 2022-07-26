from contextlib import AbstractAsyncContextManager
from sqlalchemy.ext.asyncio import AsyncSession

from {{cookiecutter.service_name}}.common.tables import BaseModel
from {{cookiecutter.service_name}}.common.db import Database


class BaseRepository:
    def __init__(self, db: Database) -> None:
        self.session_factory: [..., AbstractAsyncContextManager[AsyncSession]] = db.session
        self.db = db

    async def execute(self, query):
        return await self.db.execute(query)

    async def bulk_save(self, models: list[BaseModel]):
        return await self.db.bulk_save(models)

    async def save(self, model: BaseModel):
        return await self.db.save(model)

    async def get_or_create(self, model: BaseModel) -> BaseModel:
        return await self.db.get_or_create(model)

    async def delete(self, model: BaseModel):
        return await self.db.delete(model)

    async def truncate(self, table_name: str):
        await self.db.truncate(table_name)
