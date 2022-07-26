import ipaddress
from fastapi.logger import logger
from datetime import datetime, timedelta
from typing import Iterable, TYPE_CHECKING

from {{cookiecutter.service_name}}.common.exceptions import NotFound
from {{cookiecutter.service_name}}.modules.example.repository import ExampleRepository
from {{cookiecutter.service_name}}.modules.example.models import (

)

if TYPE_CHECKING:
    from {{cookiecutter.service_name}}.container import Repositories
    from {{cookiecutter.service_name}}.container import Gateways


class ExampleService:
    def __init__(
        self,
        repositories: 'Repositories',
        gateways: 'Gateways',
    ) -> None:
        self._example_repo: ExampleRepository = repositories.example()

    async def create_example(self, example_request: RevertRequest) -> CreateRevertResponse:
        """
        Создание заявки на реверт машины в кибербитве
        """
        try:
            if self.is_ip_address(revert_request.address):
                ip = await self._revert_repo.get_vm_ip(battle_id=battle_id, ip_address=revert_request.address)
                vm_id = ip.vm_id
            else:
                vm = await self._revert_repo.get_vm(battle_id=battle_id, fqdn=revert_request.address)
                vm_id = vm.id
        except NotFound as exc:
            logger.debug('revert.create_request address not found', exc_info=exc)
            # Save history of all requests
            await self._revert_repo.create_request(revert_request=CreateRevertRequest(
                battle_id=battle_id,
                user_id=revert_request.user_id,
                vm_not_found=True
            ))
            raise exc

        await self._revert_repo.create_request(revert_request=CreateRevertRequest(
            battle_id=battle_id,
            user_id=revert_request.user_id,
            vm_id=vm_id
        ))
        return CreateRevertResponse(revertAt=await self.get_revert_time(
            battle_id=battle_id,
            user_id=revert_request.user_id
        ))

    async def get_new_requests(self, battle_id: int) -> Iterable[NewRequests]:
        """
        Получение списка новых машин на перезапуск, с момента последнего запроса таковых
        на кибербитве
        """
        requests = await self._revert_repo.get_requests_with_vm(battle_id=battle_id)

        return (
            NewRequests(
                name=vm.name
            )
            for vm in requests
        )

    async def set_revert_statuses(self, battle_id: int, vms_info: list[StatusRequests]) -> None:
        """
        Метод для изменения статуса реверта
        """
        # TODO отбирвать куда-то уведемление о статусе false
        names = []
        for vm in vms_info:
            if vm.reverted:
                names.append(vm.name)
            else:
                print(f'{vm.name} Not reverted')
        if names:
            vms = await self._revert_repo.get_vms(battle_id=battle_id, names=names)

            if vms:
                await self._revert_repo.update_reverted(battle_id=battle_id, vm_ids=[i.id for i in vms])

    async def create_bulk_inventory_vm(self, battle_id: int) -> None:
        """
        Скачать информацию о ВМ на полигоне
        """
        inventories = await self._revert_repo.get_inventory_info(battle_id=battle_id)
        for inventory in inventories:
            vms = await self._inventory_getter.download(url=inventory.url, data_path=inventory.data_path)

            await self._revert_repo.create_or_update_vm(battle_id=battle_id, vms=vms)
