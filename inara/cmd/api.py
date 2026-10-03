import asyncio
from contextlib import asynccontextmanager, suppress

from fastapi import FastAPI

from inara.bootstrap.container import commodity_service
from inara.client import eddn
from inara.configs.setting import settings
from inara.controller.eddn.commodity import run as run_collector
from inara.controller.rest.router import api_router
from inara.pkg.logging import setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = None
    if settings.embed_collector:
        task = asyncio.create_task(
            run_collector(commodity_service(), eddn.messages(settings.eddn_url))
        )
    yield
    if task:
        task.cancel()
        with suppress(asyncio.CancelledError):
            await task


def create_app() -> FastAPI:
    setup_logging(settings.log_level)
    app = FastAPI(title="Inara", lifespan=lifespan)
    app.include_router(api_router)
    return app


app = create_app()
