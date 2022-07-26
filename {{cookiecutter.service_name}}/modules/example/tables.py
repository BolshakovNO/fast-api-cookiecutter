from sqlalchemy import Column, Integer, String, DateTime, Boolean, false, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func

from {{cookiecutter.service_name}}.common.tables import BaseModel


class ExampleTable(BaseModel):
    __tablename__ = 'example'

    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=func.now())
    last_modified = Column(DateTime, onupdate=func.now())

    value = Column(String(64))

    __table_args__ = (
        UniqueConstraint(id, value, name='example_constraint'),
    )


class ExampleChildTable(BaseModel):
    __tablename__ = 'example_child'

    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=func.now())
    last_modified = Column(DateTime, onupdate=func.now())

    value = Column(String(64))
    parent_id = Column(Integer, ForeignKey(ExampleTable.id))

    __table_args__ = (
        UniqueConstraint(id, value, parent_id, name='example_child_constraint'),
    )
