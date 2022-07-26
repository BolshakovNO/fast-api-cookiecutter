import asyncio
import typing
import logging
from contextlib import suppress


logger = logging.getLogger(__name__)


class Task:
    func = None

    def __init__(self, func: typing.Optional[typing.Callable] = None):
        if func:
            self.func = func
        elif self.func is None:
            self.func = self.method

    async def method(self, *args, **kwargs):
        raise NotImplementedError()

    async def run(self, *args, **kwargs):
        return await self.func(*args, **kwargs)


class Periodic:
    def __init__(self, func, time):
        self.func = func
        self.time = time
        self.is_started = False
        self._task = None

    async def start(self):
        if not self.is_started:
            self.is_started = True
            # Start task to call func periodically:
            self._task = asyncio.ensure_future(self._run())

    async def stop(self):
        if self.is_started:
            self.is_started = False
            # Stop task and await it stopped:
            self._task.cancel()
            with suppress(asyncio.CancelledError):
                await self._task

    async def _run(self):
        while True:
            try:
                await self.func()
            except BaseException:
                logger.exception('[ERROR] Something goes wrong')
            await asyncio.sleep(self.time)


class TasksController:
    schedule_time = 30
    delay = 0
    task_interval_delay = 0
    tasks: typing.Iterable[Task] = []

    def __init__(
        self,
        *tasks: Task,
        schedule_time: typing.Optional[int] = None,
        delay: typing.Optional[int] = None,
        task_interval_delay: typing.Optional[int] = None,
    ):
        if schedule_time is not None:
            self.schedule_time = schedule_time
        if delay is not None:
            self.delay = delay
        if task_interval_delay is not None:
            self.task_interval_delay = task_interval_delay

        self.tasks = tasks

    async def run(self) -> None:
        await asyncio.sleep(self.delay)

        for task in self.tasks:
            periodic = Periodic(task.run, self.schedule_time)
            await periodic.start()
            await asyncio.sleep(self.task_interval_delay)

