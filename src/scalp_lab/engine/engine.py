from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, List, Optional

from scalp_lab.data.tick import Tick
from scalp_lab.execution.fills import BidAskFillSimulator
from scalp_lab.execution.latency import FixedLatency, LatencyModel
from scalp_lab.execution.order import Order, OrderType
from scalp_lab.execution.slippage import FixedBpsSlippage, SlippageModel
from scalp_lab.portfolio.account import Account
from scalp_lab.strategy.base import Strategy
from .events import EventType, FillEvent, MarketEvent, OrderEvent, SignalEvent


@dataclass
class EngineConfig:
    initial_cash: float = 100_000.0
    default_order_type: OrderType = OrderType.MARKET
    fee_per_share: float = 0.0005
    latency: LatencyModel = field(default_factory=lambda: FixedLatency(ms=5.0))
    slippage: SlippageModel = field(default_factory=lambda: FixedBpsSlippage(bps=0.5))
    mark_every_n: int = 1


@dataclass
class BacktestResult:
    account: Account
    signals: int = 0
    orders: int = 0
    fills: int = 0


class BacktestEngine:
    """Event-driven backtest loop for tick scalping research.

    Pipeline per tick:
      MARKET → strategy signals → orders (+latency) → bid/ask fills → account
    """

    def __init__(
        self,
        strategy: Strategy,
        config: Optional[EngineConfig] = None,
    ) -> None:
        self.config = config or EngineConfig()
        self.strategy = strategy
        self.account = Account(cash=self.config.initial_cash)
        self.strategy.bind_account(self.account)
        self.simulator = BidAskFillSimulator(
            latency=self.config.latency,
            slippage=self.config.slippage,
            fee_per_share=self.config.fee_per_share,
        )
        self._signal_count = 0
        self._order_count = 0
        self._fill_count = 0
        self._tick_i = 0
        self.event_log: List[str] = []

    def run(self, ticks: Iterable[Tick]) -> BacktestResult:
        for tick in ticks:
            self._on_market(tick)
        if self.simulator.last_quote is not None:
            q = self.simulator.last_quote
            self.account.mark(q.symbol, q.mid, q.ts_ns)
        return BacktestResult(
            account=self.account,
            signals=self._signal_count,
            orders=self._order_count,
            fills=self._fill_count,
        )

    def _on_market(self, tick: Tick) -> None:
        self._tick_i += 1
        MarketEvent(type=EventType.MARKET, ts_ns=tick.ts_ns, tick=tick)

        fills = self.simulator.on_tick(tick)
        for fill in fills:
            self._fill_count += 1
            self.account.on_fill(fill)
            self.strategy.on_fill(fill)
            FillEvent(type=EventType.FILL, ts_ns=fill.ts_ns, fill=fill)

        signals: List[SignalEvent] = self.strategy.on_tick(tick)
        for signal in signals:
            self._signal_count += 1
            self._handle_signal(signal)

        if tick.quote is not None and self._tick_i % self.config.mark_every_n == 0:
            self.account.mark(tick.symbol, tick.quote.mid, tick.ts_ns)

    def _handle_signal(self, signal: SignalEvent) -> None:
        order = Order(
            symbol=signal.symbol,
            side=signal.side,
            qty=signal.qty,
            order_type=self.config.default_order_type,
            created_ts_ns=signal.ts_ns,
            tag=signal.reason,
        )
        self._order_count += 1
        OrderEvent(type=EventType.ORDER, ts_ns=signal.ts_ns, order=order)
        self.simulator.submit(order)
