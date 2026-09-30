import asyncio
import logging

import eddn
from db.repositories.memory import InMemoryCommodityRepository
from services.commodities import CommodityService

log = logging.getLogger(__name__)


async def main() -> None:
    service = CommodityService(InMemoryCommodityRepository())

    async for data in eddn.messages():
        if not eddn.is_commodity(data):
            continue
        try:
            prices = eddn.parse_commodity(data)
        except (KeyError, ValueError) as error:
            log.warning("Skipping malformed commodity message: %r", error)
            continue
        await service.record_market(prices)
        log.info("Recorded %d prices", len(prices))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
