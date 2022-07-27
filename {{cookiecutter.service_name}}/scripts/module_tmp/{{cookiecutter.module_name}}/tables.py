from sqlalchemy import Column, Integer, String, DateTime, Boolean, false, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func

from {{cookiecutter.service_name}}.common.tables import BaseModel


class {{cookiecutter.module_name | capitalize}}Table(BaseModel):
    __tablename__ = '{{cookiecutter.module_name}}'

    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=func.now())
    last_modified = Column(DateTime, onupdate=func.now())

    value = Column(String(64))

    __table_args__ = (
        UniqueConstraint(id, value, name='{{cookiecutter.module_name}}_constraint'),
    )
