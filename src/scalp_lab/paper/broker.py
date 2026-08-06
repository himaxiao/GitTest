from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from scalp_lab.data.tick import Quote, Side
from scalp_lab.execution.order import Fill, Order, OrderStatus, OrderType
from scalp_lab.portfolio.account import Account


@dataclass
class PaperBroker:
    """Thin paper-trading adapter sharing the same Account model.

    Wire this to a live NBBO feed later; for now it accepts manual
    quote updates and marketable orders for dry-run calibration.
    """

    account: Account = field(default_factory=Account)
    last_quotes: Dict[str, Quote] = field(default_factory=dict)
    open_orders: List[Order] = field(default_factory=list)
    fee_per_share: float = 0.0005

    def on_quote(self, quote: Quote) -> List[Fill]:
        self.last_quotes[quote.symbol] = quote
        self.account.mark(quote.symbol, quote.mid, quote.ts_ns)
        return self._match(quote)

    def submit_market(self, symbol: str, side: Side, qty: int, ts_ns: int) -> Order:
        order = Order(
            symbol=symbol,
            side=side,
            qty=qty,
            order_type=OrderType.MARKET,
            created_ts_ns=ts_ns,
            active_ts_ns=ts_ns,
            status=OrderStatus.SUBMITTED,
            tag="paper",
        )
        self.open_orders.append(order)
        quote = self.last_quotes.get(symbol)
        if quote is not None:
            fills = self._match(quote)
            # attach fills already applied in _match
            _ = fills
        return order

    def _match(self, quote: Quote) -> List[Fill]:
        fills: List[Fill] = []
        remaining: List[Order] = []
        for order in self.open_orders:
            if order.symbol != quote.symbol:
                remaining.append(order)
                continue
            if order.order_type != OrderType.MARKET:
                remaining.append(order)
                continue
            px = quote.ask if order.side == Side.BUY else quote.bid
            fill = Fill(
                order_id=order.order_id,
                symbol=order.symbol,
                side=order.side,
                qty=order.remaining,
                price=px,
                ts_ns=quote.ts_ns,
                fee=self.fee_per_share * order.remaining,
                reason="paper_market",
            )
            order.filled_qty = order.qty
            order.avg_fill_price = px
            order.status = OrderStatus.FILLED
            self.account.on_fill(fill)
            fills.append(fill)
        self.open_orders = remaining
        return fills
