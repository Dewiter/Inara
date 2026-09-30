from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.mappings.commodity import CommodityRow
from domain.commodity import CommodityPrice

class SqlCommodityRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, price: CommodityPrice) -> None:
        self.session.add(CommodityRow(**vars(price)))
        await self.session.commit()

    async def list_by_name(self, name: str) -> list[CommodityPrice]:
        rows = (await self.session.scalars(
            select(CommodityRow).where(CommodityRow.name == name)
        )).all()
        return [CommodityPrice(r.station, r.system, r.name, r.buy_price,
                               r.sell_price, r.updated_at) for r in rows]
