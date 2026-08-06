from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class Side(str, Enum):
    BUY = "BUY"
    SELL = "SELL"


@dataclass(frozen=True, slots=True)
class Quote:
    """Top-of-book quote (NBBO-style)."""

    ts_ns: int
    symbol: str
    bid: float
    ask: float
    bid_size: int
    ask_size: int

    @property
    def mid(self) -> float:
        return (self.bid + self.ask) / 2.0

    @property
    def spread(self) -> float:
        return self.ask - self.bid


@dataclass(frozen=True, slots=True)
class Trade:
    """Print / last-sale trade."""

    ts_ns: int
    symbol: str
    price: float
    size: int
    side: Optional[Side] = None  # aggressor side if known


@dataclass(frozen=True, slots=True)
class Tick:
    """Unified market event: either a quote update, a trade, or both."""

    ts_ns: int
    symbol: str
    quote: Optional[Quote] = None
    trade: Optional[Trade] = None

    def __post_init__(self) -> None:
        if self.quote is None and self.trade is None:
            raise ValueError("Tick must carry a quote and/or a trade")
