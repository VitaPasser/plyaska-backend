import logging
import traceback

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError


class ExceptionHandlers:

    def __init__(self, app: FastAPI) -> None:
        self.app = app
        self.app.add_exception_handler(Exception, self.unhandled_exception_handler)
        self.app.add_exception_handler(HTTPException,
                                       self.http_exception_handler)  # type: ignore
        self.app.add_exception_handler(ValidationError,
                                       self.validation_exception_handler)  # type: ignore
        super().__init__()

    async def http_exception_handler(self, request: Request, exc: HTTPException):
        logging.error(
            f"HTTP Exception: {exc.status_code} - {exc.detail} "
            f"on path {request.url.path}"
        )
        return JSONResponse(
            status_code=exc.status_code,
            content={"message": exc.detail},
        )

    async def validation_exception_handler(self, request: Request, exc: ValidationError):
        logging.error(
            f"HTTP Exception: 422 - {exc.errors()} "
            f"on path {request.url.path}"
        )
        return JSONResponse(status_code=422, content={"detail": exc.errors()})

    async def unhandled_exception_handler(self, request: Request, exc: Exception):
        logging.error(
            f"Unhandled Exception: {exc} "
            f"on path {request.url.path}\n{traceback.format_exc()}"
        )
        return JSONResponse(
            status_code=500,
            content={"message": "Internal Server Error"},
        )