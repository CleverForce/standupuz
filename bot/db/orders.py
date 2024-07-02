from datetime import datetime, date, time
import typing as t
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as sa_postgresql
from utils.entities_utils import save_entities
from random import randint

from .base import METADATA, begin_connection
from config import Config
from .sqlite_temp import get_options_l


class OrderRow(t.Protocol):
    id: int
    created_at: datetime
    user_id: int
    phone: str
    event_id: int
    page_id: int
    option: str
    count_place: int
    in_table: bool


OrderTable: sa.Table = sa.Table(
    "orders",
    METADATA,

    sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
    sa.Column('created_at', sa.DateTime(timezone=True)),
    sa.Column('user_id', sa.BigInteger),
    sa.Column('phone', sa.String(255)),
    sa.Column('event_id', sa.Integer),
    sa.Column('page_id', sa.BigInteger),
    sa.Column('option_name', sa.String(255)),
    sa.Column('count_place', sa.Integer),
    sa.Column('in_table', sa.Boolean, default=False),
)


# записывает новый заказ
async def add_order(user_id: int, phone: str, event_id: int, option: str, count_place: int, page_id: int) -> int:
    query = OrderTable.insert().values(
        user_id=user_id,
        phone=phone,
        event_id=event_id,
        option=option,
        count_place=count_place,
        page_id=page_id
    )
    async with begin_connection() as conn:
        result = await conn.execute(query)
    return result.inserted_primary_key[0]


# обновляет заказ
async def update_order(order_id: int, in_google: bool = None) -> None:
    query = OrderTable.update().where(OrderTable.c.id == order_id)

    if in_google is not None:
        query = query.values(in_table=in_google)
    async with begin_connection() as conn:
        await conn.execute(query)

