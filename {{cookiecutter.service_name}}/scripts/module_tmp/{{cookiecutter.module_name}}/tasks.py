import logging

from dependency_injector.wiring import inject, Provide

from {{cookiecutter.service_name}}.container import Application
from {{cookiecutter.service_name}}.common.tasks import Task, TasksController
from {{cookiecutter.service_name}}.modules.{{cookiecutter.module_name}}.service import {{cookiecutter.module_name | capitalize}}Service


logger = logging.getLogger('{{cookiecutter.module_name | capitalize}} tasks')


class {{cookiecutter.module_name | capitalize}}Task(Task):
    @inject
    async def method(
        self,
        {{cookiecutter.module_name}}_service: {{cookiecutter.module_name | capitalize}}Service = Provide[Application.services.{{cookiecutter.module_name}}]
    ) -> None:
        logger.info(f'End {{cookiecutter.module_name | capitalize}} task')


async def start_tasks():
    task = {{cookiecutter.module_name | capitalize}}Task()

    controller = TasksController(
        task,
        schedule_time=60 * 5,
        task_interval_delay=10
    )

    await controller.run()
