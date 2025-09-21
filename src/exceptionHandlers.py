import traceback
from logging import Logger

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse


class ExceptionHandlers:
    def __init__(self, logger: Logger):
        self._logger = logger

    async def http_exception_handler(self, request: Request, exc: HTTPException):
        self._logger.error(f"HTTP Exception: {exc.status_code} - {exc.detail} "
                           f"on path {request.url.path}")
        return JSONResponse(
            status_code=exc.status_code,
            content={"message": exc.detail},
        )

    async def unhandled_exception_handler(self, request: Request, exc: Exception):
        error_message = (f"Unhandled Exception: {exc} "
                         f"on path {request.url.path}\n{traceback.format_exc()}")
        self._logger.error(error_message)
        return JSONResponse(
            status_code=500,
            content={"message": "Internal Server Error"},
        )
