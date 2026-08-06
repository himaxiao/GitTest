from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Optional

from scalp_lab.data.tick import Side, Tick
from scalp_lab.execution.order import Order, Fill


class EventType(Enum):
    MARKET = auto()
    SIGNAL = auto()
    ORDER = auto()
    FILL = auto()


@dataclass
class Event:
    ts_ns: int
    type: EventType = EventType.MARKET
    payload: Any = None


@dataclass
class MarketEvent(Event):
    tick: Optional[Tick] = None

    def __post_init__(self) -> None:
        self.type = EventType.MARKET
        if self.tick is not None:
            self.ts_ns = self.tick.ts_ns
            self.payload = self.tick


@dataclass
class SignalEvent(Event):
    symbol: str = ""
    side: Side = Side.BUY
    strength: float = 1.0
    qty: int = 100
    reason: str = ""

    def __post_init__(self) -> None:
        self.type = EventType.SIGNAL
        self.payload = {
            "symbol": self.symbol,
            "side": self.side,
            "strength": self.strength,
            "qty": self.qty,
            "reason": self.reason,
        }


@dataclass
class OrderEvent(Event):
    order: Optional[Order] = None

    def __post_init__(self) -> None:
        self.type = EventType.ORDER
        if self.order is not None:
            self.ts_ns = self.order.created_ts_ns
            self.payload = self.order


@dataclass
class FillEvent(Event):
    fill: Optional[Fill] = None

    def __post_init__(self) -> None:
        self.type = EventType.FILL
        if self.fill is not None:
            self.ts_ns = self.fill.ts_ns
            self.payload = self.fill
