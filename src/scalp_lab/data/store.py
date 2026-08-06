from __future__ import annotations

from pathlib import Path
from typing import Iterable, Iterator, List, Optional

import pandas as pd

from .tick import Quote, Tick, Trade


class TickStore:
    """In-memory / parquet tick store.

    Expected parquet / dataframe columns:
      ts_ns, symbol, bid, ask, bid_size, ask_size, trade_price, trade_size
    Empty trade_price means quote-only tick.
    """

    def __init__(self, ticks: Optional[List[Tick]] = None) -> None:
        self._ticks: List[Tick] = sorted(ticks or [], key=lambda t: t.ts_ns)

    @classmethod
    def from_dataframe(cls, df: pd.DataFrame) -> "TickStore":
        ticks: List[Tick] = []
        for row in df.itertuples(index=False):
            quote = None
            trade = None
            bid = getattr(row, "bid", None)
            ask = getattr(row, "ask", None)
            if bid is not None and ask is not None and pd.notna(bid) and pd.notna(ask):
                quote = Quote(
                    ts_ns=int(row.ts_ns),
                    symbol=str(row.symbol),
                    bid=float(bid),
                    ask=float(ask),
                    bid_size=int(getattr(row, "bid_size", 100) or 100),
                    ask_size=int(getattr(row, "ask_size", 100) or 100),
                )
            trade_price = getattr(row, "trade_price", None)
            trade_size = getattr(row, "trade_size", None)
            if trade_price is not None and pd.notna(trade_price):
                trade = Trade(
                    ts_ns=int(row.ts_ns),
                    symbol=str(row.symbol),
                    price=float(trade_price),
                    size=int(trade_size or 100),
                )
            if quote is not None or trade is not None:
                ticks.append(
                    Tick(ts_ns=int(row.ts_ns), symbol=str(row.symbol), quote=quote, trade=trade)
                )
        return cls(ticks)

    @classmethod
    def from_parquet(cls, path: str | Path) -> "TickStore":
        return cls.from_dataframe(pd.read_parquet(path))

    def to_dataframe(self) -> pd.DataFrame:
        rows = []
        for t in self._ticks:
            rows.append(
                {
                    "ts_ns": t.ts_ns,
                    "symbol": t.symbol,
                    "bid": t.quote.bid if t.quote else None,
                    "ask": t.quote.ask if t.quote else None,
                    "bid_size": t.quote.bid_size if t.quote else None,
                    "ask_size": t.quote.ask_size if t.quote else None,
                    "trade_price": t.trade.price if t.trade else None,
                    "trade_size": t.trade.size if t.trade else None,
                }
            )
        return pd.DataFrame(rows)

    def append(self, ticks: Iterable[Tick]) -> None:
        self._ticks.extend(ticks)
        self._ticks.sort(key=lambda t: t.ts_ns)

    def __iter__(self) -> Iterator[Tick]:
        return iter(self._ticks)

    def __len__(self) -> int:
        return len(self._ticks)

    def filter_symbol(self, symbol: str) -> "TickStore":
        return TickStore([t for t in self._ticks if t.symbol == symbol])
