from fastapi import APIRouter
from controllers import commodities

api_router = APIRouter()
api_router.include_router(commodities.router)
