from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from db.repositories.commodity import SqlCommodityRepository
from services.commodities import CommodityService

engine = create_async_engine("postgresql+asyncpg://user:pass@localhost/inara")
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def get_session():
    async with SessionLocal() as session:
        yield session


def get_commodity_service(
    session: AsyncSession = Depends(get_session),
) -> CommodityService:...
    # return CommodityService(SqlCommodityRepository(session))
