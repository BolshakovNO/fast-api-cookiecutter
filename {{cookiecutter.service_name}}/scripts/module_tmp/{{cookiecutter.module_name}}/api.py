from typing import Iterable

from fastapi import Depends, Path
from dependency_injector.wiring import inject, Provide

from {{cookiecutter.service_name}}.container import Application
from {{cookiecutter.service_name}}.common.models import OnlyId
from {{cookiecutter.service_name}}.modules.{{cookiecutter.module_name}}.models import (
    {{cookiecutter.module_name | capitalize}}
)
from {{cookiecutter.service_name}}.modules.{{cookiecutter.module_name}}.service import {{cookiecutter.module_name | capitalize}}Service
from {{cookiecutter.service_name}}.common.router import ServiceAPIRouter


router = ServiceAPIRouter(prefix='/{{cookiecutter.module_name}}', tags=['{{cookiecutter.module_name}}'])


@router.post('', response_model=OnlyId, description="""
    Пример POST запроса
""")
@inject
async def create_{{cookiecutter.module_name}}(
    {{cookiecutter.module_name}}: {{cookiecutter.module_name | capitalize}},
    {{cookiecutter.module_name}}_service: {{cookiecutter.module_name | capitalize}}Service = Depends(Provide[Application.services.{{cookiecutter.module_name}}]),
) -> OnlyId:
    return await {{cookiecutter.module_name}}_service.create_{{cookiecutter.module_name}}({{cookiecutter.module_name}}_request={{cookiecutter.module_name}})
