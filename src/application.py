from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from src.exceptions.handlers import setup_exception_handlers
from src.router.healthcheck import router as healthcheck_router
from src.router.v1 import router as v1_router


def setup_routers(app: FastAPI) -> None:
    app.include_router(v1_router)
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

    setup_exception_handlers(app)

    setup_routers(app)

    return app
