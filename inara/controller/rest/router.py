from fastapi import APIRouter

from inara.controller.rest import commodity

api_router = APIRouter()
api_router.include_router(commodity.router)
