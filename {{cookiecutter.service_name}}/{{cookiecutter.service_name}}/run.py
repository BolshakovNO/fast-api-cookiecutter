import asyncio
import logging
import uvicorn

from {{cookiecutter.service_name}}.main import app
from {{cookiecutter.service_name}}.modules.revert.tasks import start_tasks


async def run_tasks(loop):
    await loop.create_task(start_tasks())


@app.on_event("startup")
async def startup_event():
    logger = logging.getLogger("uvicorn.access")
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)


if __name__ == '__main__':
    config = app.container.config()
    if bool(config['core']['app']['run_app']):
        uvicorn.run(
            '{{cookiecutter.service_name}}.main:app',
            host='0.0.0.0',
            port=8000,
            workers=int(config['core']['app']['workers']),
            access_log=True
        )
    elif bool(config['core']['tasks']['run_tasks']):
        policy = asyncio.get_event_loop_policy()
        loop = policy.get_event_loop()
        loop.run_until_complete(run_tasks(loop))
        loop.run_forever()
