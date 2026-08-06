from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from typing import Deque, List, Optional

from scalp_lab.data.synthetic import estimate_microprice
from scalp_lab.data.tick import Side, Tick
from scalp_lab.engine.events import SignalEvent
from scalp_lab.execution.order import Fill
from .base import Strategy


@dataclass
class MicropriceScalp(Strategy):
    """Toy scalp: trade microprice dislocation vs mid.

    Wiring example only — not a production alpha.
    Enters on |z| spike, exits on mean reversion or max hold.
    """

    symbol: str = "AAPL"
    lookback: int = 20
    entry_z: float = 1.5
    qty: int = 100
    max_hold_ticks: int = 40

    _mids: Deque[float] = field(default_factory=deque, init=False, repr=False)
    _micros: Deque[float] = field(default_factory=deque, init=False, repr=False)
    _hold_ticks: int = field(default=0, init=False, repr=False)

    def __post_init__(self) -> None:
        Strategy.__init__(self, self.symbol)
        self._mids = deque(maxlen=self.lookback)
        self._micros = deque(maxlen=self.lookback)

    def on_tick(self, tick: Tick) -> List[SignalEvent]:
        if tick.symbol != self.symbol or tick.quote is None:
            return []

        q = tick.quote
        micro = estimate_microprice(q)
        self._mids.append(q.mid)
        self._micros.append(micro)

        signals: List[SignalEvent] = []
        pos_qty = 0
        if self.account is not None:
            pos_qty = self.account.position(self.symbol).qty

        if pos_qty != 0:
            self._hold_ticks += 1
            dislocation = micro - q.mid
            should_exit = self._hold_ticks >= self.max_hold_ticks
            if pos_qty > 0 and dislocation <= 0:
                should_exit = True
            if pos_qty < 0 and dislocation >= 0:
                should_exit = True
            if should_exit:
                side = Side.SELL if pos_qty > 0 else Side.BUY
                signals.append(
                    SignalEvent(
                        ts_ns=tick.ts_ns,
                        symbol=self.symbol,
                        side=side,
                        qty=abs(pos_qty),
                        reason="exit",
                    )
                )
                self._hold_ticks = 0
            return signals

        if len(self._mids) < self.lookback:
            return []

        diffs = [m - mid for m, mid in zip(self._micros, self._mids)]
        mean = sum(diffs) / len(diffs)
        var = sum((d - mean) ** 2 for d in diffs) / max(len(diffs) - 1, 1)
        std = var**0.5
        if std < 1e-8:
            return []
        z = (diffs[-1] - mean) / std

        if z >= self.entry_z:
            signals.append(
                SignalEvent(
                    ts_ns=tick.ts_ns,
                    symbol=self.symbol,
                    side=Side.BUY,
                    qty=self.qty,
                    strength=z,
                    reason=f"micro_z={z:.2f}",
                )
            )
            self._hold_ticks = 0
        elif z <= -self.entry_z:
            signals.append(
                SignalEvent(
                    ts_ns=tick.ts_ns,
                    symbol=self.symbol,
                    side=Side.SELL,
                    qty=self.qty,
                    strength=z,
                    reason=f"micro_z={z:.2f}",
                )
            )
            self._hold_ticks = 0

        return signals

    def on_fill(self, fill: Fill) -> None:
        return None
