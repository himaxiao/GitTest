from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from scalp_lab.data.tick import Side
from scalp_lab.execution.order import Fill


@dataclass
class Position:
    symbol: str
    qty: int = 0
    avg_price: float = 0.0
    realized_pnl: float = 0.0

    def apply_fill(self, fill: Fill) -> float:
        """Apply fill; return realized PnL delta (before fees)."""
        signed = fill.qty if fill.side == Side.BUY else -fill.qty
        realized = 0.0

        if self.qty == 0 or (self.qty > 0 and signed > 0) or (self.qty < 0 and signed < 0):
            # Increasing / opening same direction
            new_qty = self.qty + signed
            if new_qty != 0:
                self.avg_price = (
                    (abs(self.qty) * self.avg_price + fill.qty * fill.price) / abs(new_qty)
                )
            self.qty = new_qty
        else:
            # Reducing / flipping
            close_qty = min(abs(self.qty), fill.qty)
            direction = 1 if self.qty > 0 else -1
            realized = direction * (fill.price - self.avg_price) * close_qty
            self.qty += signed
            if self.qty == 0:
                self.avg_price = 0.0
            elif (self.qty > 0 and signed > 0) or (self.qty < 0 and signed < 0):
                # flipped and residual is new position at fill price
                self.avg_price = fill.price
            self.realized_pnl += realized

        return realized


@dataclass
class Account:
    cash: float = 100_000.0
    positions: Dict[str, Position] = field(default_factory=dict)
    fills: List[Fill] = field(default_factory=list)
    equity_curve: List[tuple[int, float]] = field(default_factory=list)
    fees_paid: float = 0.0
    realized_pnl: float = 0.0
    _last_mids: Dict[str, float] = field(default_factory=dict)

    def position(self, symbol: str) -> Position:
        if symbol not in self.positions:
            self.positions[symbol] = Position(symbol=symbol)
        return self.positions[symbol]

    def on_fill(self, fill: Fill) -> None:
        pos = self.position(fill.symbol)
        realized = pos.apply_fill(fill)
        self.realized_pnl += realized
        self.fees_paid += fill.fee
        notional = fill.price * fill.qty
        if fill.side == Side.BUY:
            self.cash -= notional + fill.fee
        else:
            self.cash += notional - fill.fee
        self.fills.append(fill)

    def mark(self, symbol: str, mid: float, ts_ns: int) -> None:
        self._last_mids[symbol] = mid
        self.equity_curve.append((ts_ns, self.equity()))

    def unrealized_pnl(self) -> float:
        total = 0.0
        for sym, pos in self.positions.items():
            mid = self._last_mids.get(sym)
            if mid is None or pos.qty == 0:
                continue
            total += pos.qty * (mid - pos.avg_price)
        return total

    def equity(self) -> float:
        # Cash already includes realized PnL and fees; add open MTM.
        return self.cash + self.unrealized_pnl()
