from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from uuid import uuid4

from scalp_lab.data.tick import Side


class OrderType(str, Enum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"


class OrderStatus(str, Enum):
    NEW = "NEW"
    SUBMITTED = "SUBMITTED"
    PARTIAL = "PARTIAL"
    FILLED = "FILLED"
    CANCELLED = "CANCELLED"
    REJECTED = "REJECTED"


@dataclass(slots=True)
class Order:
    symbol: str
    side: Side
    qty: int
    order_type: OrderType
    created_ts_ns: int
    limit_price: Optional[float] = None
    order_id: str = field(default_factory=lambda: uuid4().hex[:12])
    status: OrderStatus = OrderStatus.NEW
    filled_qty: int = 0
    avg_fill_price: float = 0.0
    # When the order becomes active after latency
    active_ts_ns: Optional[int] = None
    tag: str = ""

    @property
    def remaining(self) -> int:
        return self.qty - self.filled_qty


@dataclass(slots=True)
class Fill:
    order_id: str
    symbol: str
    side: Side
    qty: int
    price: float
    ts_ns: int
    fee: float = 0.0
    slippage: float = 0.0
    latency_ns: int = 0
    mid_at_signal: Optional[float] = None
    reason: str = ""
