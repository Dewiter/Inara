from fastapi import APIRouter, Depends
from pydantic import BaseModel

from dependencies import get_commodity_service
from services.commodities import CommodityService

router = APIRouter(prefix="/commodities", tags=["commodities"])

class PriceOut(BaseModel):
    station: str
    system: str
    sell_price: int


@router.get("/{name}/best-sell", response_model=list[PriceOut])
async def best_sell(name: str, svc: CommodityService = Depends(get_commodity_service)):
    return await svc.best_sell_locations(name)
