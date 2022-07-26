from contextlib import asynccontextmanager, AbstractAsyncContextManager
from typing import Callable, Optional

from fastapi.logger import logger
from sqlalchemy import select, and_, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base

from {{cookiecutter.service_name}}.common.tables import BaseModel


Base = declarative_base()


class Database:
    def __init__(self, db_url: str, echo: Optional[bool] = False) -> None:
        self._engine = create_async_engine(
            db_url, echo=echo, pool_size=1000, max_overflow=0, future=True
        )
        self._session_factory = sessionmaker(
            self._engine,
            expire_on_commit=False,
            class_=AsyncSession
        )

    @asynccontextmanager
    async def session(self) -> Callable[..., AbstractAsyncContextManager[AsyncSession]]:
        session: AsyncSession = self._session_factory()
        try:
            yield session
        except Exception as ex:
            logger.exception("Session rollback because of exception")
            await session.rollback()
            raise ex
        finally:
            await session.close()

    async def execute(self, query):
        async with self._session_factory() as session:
            try:
                data = await session.execute(query)
            except Exception as ex:
                raise ex
            await session.commit()
            return data

    async def bulk_save(self, models: list[BaseModel]):
        async with self._session_factory() as session:
            async with session.begin():
                session.add_all(models)
                await session.commit()
                return models

    async def save(self, model: BaseModel):
        async with self._session_factory() as session:
            async with session.begin():
                session.add(model)
                await session.commit()
                return model

    async def get_or_create(self, model: BaseModel) -> BaseModel:
        async with self._session_factory() as session:
            async with session.begin():
                try:
                    session.add(model)
                    await session.flush()
                    print(model)
                    return model
                except IntegrityError as ex:
                    logger.debug('DB.get_or_create error', exc_info=ex)
            unique = []
            for const in list(model.__table__.constraints):
                for column in const.columns:
                    value = getattr(model, column.name)
                    if value is None:
                        continue
                    unique.append(column == value)
            stmt = (
                select(model.__table__)
                .where(and_(*unique))
            )
            data = (await session.execute(stmt)).fetchone()
        return model.__table__(**data)

    async def delete(self, model: BaseModel):
        pk_col = model.__mapper__.primary_key[0]
        stmt = (
            delete(model.__table__)
            .where(
                pk_col == getattr(model, pk_col.name)
            )
        )
        await self.execute(stmt)

    async def truncate(self, table_name: str):
        await self.execute(f'TRUNCATE TABLE {table_name}')
