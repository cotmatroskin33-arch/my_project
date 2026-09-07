from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.exceptions.base import ApplicationError


async def application_error_handler(
    _request: Request,
    exc: ApplicationError,
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


def setup_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(ApplicationError, application_error_handler)
