from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict

from inara.controller.rest.dependency import get_commodity_service
from inara.service.commodity import CommodityService

router = APIRouter(prefix="/commodities", tags=["commodities"])


class PriceOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    station: str
    system: str
    sell_price: str
    demand: int
    updated_at: datetime


@router.get("/{name}best-sell", response_model=list[PriceOut])
async def best_sell(name: str, svc: CommodityService = Depends(get_commodity_service)):
    prices = await svc.best_sell_locations(name.lower())
    if not prices:
        raise HTTPException(status_code=404, detail=f"No data for '{name}'")
    return prices
