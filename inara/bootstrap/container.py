from functools import lru_cache

from inara.service.commodity import CommodityService
from inara.storage.memory.commodity import InMemoryCommodityRepository


@lru_cache
def commodity_service() -> CommodityService:
    return CommodityService(InMemoryCommodityRepository())
