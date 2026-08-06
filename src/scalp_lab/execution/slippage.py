from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Protocol

from scalp_lab.data.tick import Quote, Side


class SlippageModel(Protocol):
    def apply(
        self,
        side: Side,
        qty: int,
        quote: Quote,
        base_price: float,
    ) -> tuple[float, float]:
        """Return (fill_price, slippage_vs_base)."""
        ...


@dataclass(slots=True)
class FixedBpsSlippage:
    """Extra cost in basis points beyond crossing the spread."""

    bps: float = 0.5

    def apply(
        self,
        side: Side,
        qty: int,
        quote: Quote,
        base_price: float,
    ) -> tuple[float, float]:
        mult = self.bps / 10_000.0
        if side == Side.BUY:
            px = base_price * (1.0 + mult)
        else:
            px = base_price * (1.0 - mult)
        slip = abs(px - base_price)
        return round(px, 4), round(slip, 6)


@dataclass(slots=True)
class SpreadAwareSlippage:
    """Partial-spread + size impact vs displayed size."""

    extra_spread_frac: float = 0.0
    impact_bps_per_displayed: float = 2.0

    def apply(
        self,
        side: Side,
        qty: int,
        quote: Quote,
        base_price: float,
    ) -> tuple[float, float]:
        displayed = quote.ask_size if side == Side.BUY else quote.bid_size
        ratio = qty / max(displayed, 1)
        impact = (self.impact_bps_per_displayed / 10_000.0) * ratio * base_price
        spread_extra = self.extra_spread_frac * quote.spread
        if side == Side.BUY:
            px = base_price + impact + spread_extra
        else:
            px = base_price - impact - spread_extra
        slip = abs(px - base_price)
        return round(px, 4), round(slip, 6)


@dataclass(slots=True)
class ZeroSlippage:
    def apply(
        self,
        side: Side,
        qty: int,
        quote: Quote,
        base_price: float,
    ) -> tuple[float, float]:
        return base_price, 0.0
