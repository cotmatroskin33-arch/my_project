from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.exceptions import ApplicationError
from src.router.books import router as books_router
from src.router.healthcheck import router as healthcheck_router


async def application_error_handler(
    _request: Request,
    exc: ApplicationError,
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


def setup_routers(app: FastAPI) -> None:
    app.include_router(books_router)
    app.include_router(healthcheck_router)


def get_app() -> FastAPI:
    app = FastAPI(
        docs_url='/docs',
        openapi_url='/openapi.json',
        default_response_class=JSONResponse,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    app.add_exception_handler(ApplicationError, application_error_handler)

    setup_routers(app)

    return app
