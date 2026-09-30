from datetime import datetime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase): ...


class CommodityRow(Base):
    __tablename__ = "commodity_prices"
    id: Mapped[int] = mapped_column(primary_key=True)
    station: Mapped[str]
    system: Mapped[str]
    name: Mapped[str] = mapped_column(index=True)
    buy_price: Mapped[int]
    sell_price: Mapped[int]
    updated_at: Mapped[datetime]
