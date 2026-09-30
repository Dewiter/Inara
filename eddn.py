import json
import logging
import zlib
from collections.abc import AsyncIterator
from datetime import datetime

import zmq
import zmq.asyncio

from domain.commodity import CommodityPrice

log = logging.getLogger(__name__)

EDDN_URL = "tcp://eddn.edcd.io:9500"
COMMODITY_SCHEMA_PREFIX = "https://eddn.edcd.io/schemas/commodity/"


async def messages() -> AsyncIterator[dict]:
    """Yield decoded EDDN envelopes forever."""
    context = zmq.asyncio.Context()
    socket = context.socket(zmq.SUB)
    socket.connect(EDDN_URL)
    socket.setsockopt_string(zmq.SUBSCRIBE, "")
    log.info("Connected to EDDN")

    while True:
        raw = await socket.recv()
        try:
            yield json.loads(zlib.decompress(raw))
        except (zlib.error, json.JSONDecodeError) as error:
            log.warning("Could not decode EDDN message: %s", error)


def is_commodity(data: dict) -> bool:
    return data.get("$schemaRef", "").startswith(COMMODITY_SCHEMA_PREFIX)


def parse_commodity(data: dict) -> list[CommodityPrice]:
    """Translate an EDDN commodity envelope into domain objects."""
    msg = data["message"]
    updated_at = datetime.fromisoformat(msg["timestamp"])
    return [
        CommodityPrice(
            market_id=msg["marketId"],
            station=msg["stationName"],
            system=msg["systemName"],
            name=c["name"],
            buy_price=c["buyPrice"],
            sell_price=c["sellPrice"],
            stock=c["stock"],
            demand=c["demand"],
            updated_at=updated_at,
        )
        for c in msg["commodities"]
    ]
