from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Protocol

from scalp_lab.data.tick import Quote, Side, Tick
from .latency import FixedLatency, LatencyModel
from .order import Fill, Order, OrderStatus, OrderType
from .slippage import FixedBpsSlippage, SlippageModel


class FillSimulator(Protocol):
    def on_tick(self, tick: Tick) -> List[Fill]:
        ...

    def submit(self, order: Order) -> None:
        ...


@dataclass
class BidAskFillSimulator:
    """Simulate fills against top-of-book bid/ask with latency + slippage.

    Market buy crosses ask; market sell crosses bid.
    Limit orders fill only when price is marketable against the book.
    Partial fills limited by displayed size on the touched side.
    """

    latency: LatencyModel = field(default_factory=FixedLatency)
    slippage: SlippageModel = field(default_factory=FixedBpsSlippage)
    fee_per_share: float = 0.0005
    last_quote: Optional[Quote] = None
    pending: List[Order] = field(default_factory=list)

    def submit(self, order: Order) -> None:
        delay = self.latency.delay_ns(order.created_ts_ns)
        order.active_ts_ns = order.created_ts_ns + delay
        order.status = OrderStatus.SUBMITTED
        self.pending.append(order)

    def on_tick(self, tick: Tick) -> List[Fill]:
        if tick.quote is not None:
            self.last_quote = tick.quote
        if self.last_quote is None:
            return []

        fills: List[Fill] = []
        still_pending: List[Order] = []

        for order in self.pending:
            if order.active_ts_ns is not None and tick.ts_ns < order.active_ts_ns:
                still_pending.append(order)
                continue
            if order.symbol != tick.symbol:
                still_pending.append(order)
                continue

            fill = self._try_fill(order, tick.ts_ns, self.last_quote)
            if fill is None:
                still_pending.append(order)
                continue

            fills.append(fill)
            order.filled_qty += fill.qty
            # running avg
            prev = order.avg_fill_price * (order.filled_qty - fill.qty)
            order.avg_fill_price = (prev + fill.price * fill.qty) / order.filled_qty
            if order.remaining > 0:
                order.status = OrderStatus.PARTIAL
                still_pending.append(order)
            else:
                order.status = OrderStatus.FILLED

        self.pending = still_pending
        return fills

    def _try_fill(self, order: Order, ts_ns: int, quote: Quote) -> Optional[Fill]:
        if order.order_type == OrderType.MARKET:
            base = quote.ask if order.side == Side.BUY else quote.bid
            available = quote.ask_size if order.side == Side.BUY else quote.bid_size
        else:
            # LIMIT
            if order.limit_price is None:
                order.status = OrderStatus.REJECTED
                return None
            if order.side == Side.BUY:
                if quote.ask > order.limit_price:
                    return None
                base = min(quote.ask, order.limit_price)
                available = quote.ask_size
            else:
                if quote.bid < order.limit_price:
                    return None
                base = max(quote.bid, order.limit_price)
                available = quote.bid_size

        qty = min(order.remaining, max(available, 0))
        if qty <= 0:
            return None

        px, slip = self.slippage.apply(order.side, qty, quote, base)
        # Keep limit orders from sliding through limit
        if order.order_type == OrderType.LIMIT and order.limit_price is not None:
            if order.side == Side.BUY:
                px = min(px, order.limit_price)
            else:
                px = max(px, order.limit_price)

        latency_ns = (order.active_ts_ns or order.created_ts_ns) - order.created_ts_ns
        return Fill(
            order_id=order.order_id,
            symbol=order.symbol,
            side=order.side,
            qty=qty,
            price=px,
            ts_ns=ts_ns,
            fee=round(self.fee_per_share * qty, 6),
            slippage=slip,
            latency_ns=latency_ns,
            mid_at_signal=quote.mid,
            reason="bid_ask_cross" if order.order_type == OrderType.MARKET else "limit_touch",
        )
