import logging.config
from pathlib import Path

from dependency_injector import containers, providers

from {{cookiecutter.service_name}}.common.db import Database
from {{cookiecutter.service_name}}.modules.example.service import ExampleService
from {{cookiecutter.service_name}}.modules.example.repository import ExampleRepository


CONFIG_PATH = str(Path(__file__).parent / "config.yml")


class Core(containers.DeclarativeContainer):

    config = providers.Configuration(yaml_files=[CONFIG_PATH])

    # logging = providers.Resource(
    #     logging.config.dictConfig,
    #     config=config.logging,
    # )


class Gateways(containers.DeclarativeContainer):

    config = providers.Configuration(yaml_files=[CONFIG_PATH])

    db = providers.Resource(
        Database,
        db_url=config.db.url,
        echo=config.db.echo,
    )


class Repositories(containers.DeclarativeContainer):
    config = providers.Configuration(yaml_files=[CONFIG_PATH])

    gateways = providers.DependenciesContainer()

    example = providers.Factory(
        ExampleRepository,
        db=gateways.db,
    )


class Services(containers.DeclarativeContainer):

    config = providers.Configuration(yaml_files=[CONFIG_PATH])

    repositories = providers.DependenciesContainer()
    gateways = providers.DependenciesContainer()

    example = providers.Factory(
        ExampleService,
        repositories=repositories,
        gateways=gateways,
    )


class Application(containers.DeclarativeContainer):

    config = providers.Configuration(yaml_files=[CONFIG_PATH])

    core = providers.Container(
        Core,
        config=config.core,
    )

    gateways = providers.Container(
        Gateways,
        config=config.gateways,
    )

    repositories = providers.Container(
        Repositories,
        config=config.gateways,
        gateways=gateways,
    )

    services = providers.Container(
        Services,
        config=config.services,
        repositories=repositories,
        gateways=gateways,
    )
