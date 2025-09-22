import logging
import traceback

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse


class ExceptionHandlers:
    async def http_exception_handler(self, request: Request, exc: HTTPException):
        logging.error(f"HTTP Exception: {exc.status_code} - {exc.detail} "
                      f"on path {request.url.path}")
        return JSONResponse(
            status_code=exc.status_code,
            content={"message": exc.detail},
        )

    async def unhandled_exception_handler(self, request: Request, exc: Exception):
        logging.error(f"Unhandled Exception: {exc} "
                      f"on path {request.url.path}\n{traceback.format_exc()}")
        return JSONResponse(
            status_code=500,
            content={"message": "Internal Server Error"},
        )
