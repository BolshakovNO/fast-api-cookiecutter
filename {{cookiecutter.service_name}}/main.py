from pathlib import Path

from fastapi import FastAPI

import {{cookiecutter.service_name}}.modules
import {{cookiecutter.service_name}}.modules.external
import {{cookiecutter.service_name}}.common
from {{cookiecutter.service_name}}.container import Application
from {{cookiecutter.service_name}}.modules.example.api import router as example_router

from {{cookiecutter.service_name}}.middlewares import ErrorsMiddleware


CONFIG_PATH = str(Path(__file__).parent / "config.yml")


def create_app() -> FastAPI:
    application = Application()
    application.init_resources()
    application.wire(packages=[
        {{cookiecutter.service_name}}.modules.example,
    ])

    app = FastAPI(
        title='STF {{cookiecutter.service_name}}',
        description='API {{cookiecutter.service_name}} The Standoff 365',
        version='0.1.0',
        debug=application.config()['core']['debug']
    )
    app.add_middleware(ErrorsMiddleware)

    app.container = application
    app.include_router(example_router)

    return app


app = create_app()
