from fastapi import Request, Response
from fastapi.logger import logger
from starlette.middleware.base import BaseHTTPMiddleware

from {{cookiecutter.service_name}}.common.exceptions import ServiceBaseException


class ErrorsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except ServiceBaseException as exc:
            logger.exception(exc.msg)
            return Response(status_code=exc.status_code, content=exc.msg)
