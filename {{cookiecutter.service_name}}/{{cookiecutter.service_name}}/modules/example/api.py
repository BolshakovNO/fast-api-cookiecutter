from typing import Iterable

from fastapi import Depends, Path
from dependency_injector.wiring import inject, Provide

from {{cookiecutter.service_name}}.container import Application
from {{cookiecutter.service_name}}.common.models import OnlyId
from {{cookiecutter.service_name}}.modules.example.models import (
    CreateExample, Example, ExampleParent
)
from {{cookiecutter.service_name}}.modules.example.service import ExampleService
from {{cookiecutter.service_name}}.common.router import ServiceAPIRouter


router = ServiceAPIRouter(prefix='/example', tags=['example'])


@router.post('', response_model=OnlyId, description="""
    Пример POST запроса
""")
@inject
async def create_example(
    example: CreateExample,
    example_service: ExampleService = Depends(Provide[Application.services.example]),
) -> OnlyId:
    return await example_service.create_example(example_request=example)


@router.get('/{id}/children', response_model=Example, description="""
    Пример GET запроса, с получением дочерних сущностей
""")
@inject
async def get_example_with_children(
    id: int = Path(),
    example_service: ExampleService = Depends(Provide[Application.services.example]),
) -> Example:
    return await example_service.get_example_with_children(id=id)


@router.get('/{id}', response_model=ExampleParent, description="""
    Пример GET запроса
""")
@inject
async def get_example(
    id: int = Path(),
    example_service: ExampleService = Depends(Provide[Application.services.example]),
) -> ExampleParent:
    return await example_service.get_example(id=id)
