from typing import Iterable

from fastapi import Depends, Path
from dependency_injector.wiring import inject, Provide

from {{cookiecutter.service_name}}.container import Application
from {{cookiecutter.service_name}}.modules.revert.models import (
    RevertRequest
)
from {{cookiecutter.service_name}}.modules.revert.service import RevertService
from {{cookiecutter.service_name}}.common.router import ServiceAPIRouter


router = ServiceAPIRouter(prefix='/example', tags=['example'])


@router.get('/example/{id}', response_model=list[NewRequests], description="""
    Метод получения новых машин на перезапуск с момента последнего запроса на кибербитве.
""")
@inject
async def get_new_requests(
    battle_id: int = Path(),
    revert_service: RevertService = Depends(Provide[Application.services.revert]),
) -> Iterable[NewRequests]:
    return await revert_service.get_new_requests(battle_id=battle_id)


@router.post('/cyberbattle/{battle_id}/status', description="""
    Метод обновления статусов запросов на revert по признаку
""")
@inject
async def set_revert_status(
    vms_info: list[StatusRequests],
    battle_id: int = Path(),
    revert_service: RevertService = Depends(Provide[Application.services.revert]),
) -> None:
    return await revert_service.set_revert_statuses(battle_id=battle_id, vms_info=vms_info)


@router.post('/cyberbattle/{battle_id}', response_model=CreateRevertResponse, description="""
    Метод создания новых заявок на перезапуск машины на кибербитве
""")
@inject
async def create_new_revert_request(
    revert_request: RevertRequest,
    battle_id: int = Path(),
    revert_service: RevertService = Depends(Provide[Application.services.revert]),
) -> CreateRevertResponse:
    return await revert_service.create_request(revert_request=revert_request, battle_id=battle_id)
