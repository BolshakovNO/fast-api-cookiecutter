import logging

from dependency_injector.wiring import inject, Provide

from {{cookiecutter.service_name}}.container import Application
from {{cookiecutter.service_name}}.common.tasks import Task, TasksController
from {{cookiecutter.service_name}}.modules.example.service import ExampleService


logger = logging.getLogger('example tasks')


class ExampleTask(Task):
    @inject
    async def method(
        self,
        example_service: ExampleService = Provide[Application.services.example]
    ) -> None:
        await example_service.get_example()
        logger.info(f'End example task')


async def start_tasks():
    example = ExampleTask(battle_id=7)

    controller = TasksController(
        example,
        schedule_time=60 * 5,
        task_interval_delay=10
    )

    await controller.run()
