import asyncio

from inara.bootstrap.container import commodity_service
from inara.client import eddn
from inara.configs.setting import settings
from inara.controller.eddn.commodity import run
from inara.pkg.logging import setup_logging


def main() -> None:
    setup_logging(settings.log_level)
    asyncio.run(run(commodity_service(), eddn.messages(settings.eddn_url)))


if __name__ == "__main__":
    main()
