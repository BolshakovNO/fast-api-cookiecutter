import logging

from fastapi import APIRouter


class ServiceAPIRouter(APIRouter):
    logger = logging.getLogger()
