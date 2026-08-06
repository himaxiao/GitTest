from __future__ import annotations

from typing import List

import numpy as np

from .tick import Quote, Tick, Trade


def generate_synthetic_ticks(
    symbol: str = "AAPL",
    n_ticks: int = 5_000,
    start_price: float = 190.0,
    start_ts_ns: int = 1_700_000_000_000_000_000,
    tick_interval_ns: int = 50_000_000,  # 50ms
    spread: float = 0.01,
    volatility: float = 0.00015,
    seed: int = 42,
) -> List[Tick]:
    """Generate realistic-enough NBBO + trades for local research demos.

    Not a market simulator for live alpha — only for wiring the pipeline.
    """
    rng = np.random.default_rng(seed)
    mid = float(start_price)
    ticks: List[Tick] = []
    ts = start_ts_ns

    for i in range(n_ticks):
        # Mean-reverting micro moves with occasional burst
        shock = rng.normal(0.0, volatility * mid)
        if rng.random() < 0.02:
            shock *= 4.0
        mid = max(0.01, mid + shock)
        half = spread / 2.0
        bid = round(mid - half, 4)
        ask = round(mid + half, 4)
        bid_size = int(rng.integers(100, 2000) // 100 * 100)
        ask_size = int(rng.integers(100, 2000) // 100 * 100)

        quote = Quote(
            ts_ns=ts,
            symbol=symbol,
            bid=bid,
            ask=ask,
            bid_size=bid_size,
            ask_size=ask_size,
        )

        trade = None
        if rng.random() < 0.35:
            # Trade at bid/ask/mid with slight noise
            side_roll = rng.random()
            if side_roll < 0.45:
                px = ask
            elif side_roll < 0.90:
                px = bid
            else:
                px = round(mid, 4)
            size = int(rng.integers(1, 20) * 100)
            trade = Trade(ts_ns=ts, symbol=symbol, price=px, size=size)

        ticks.append(Tick(ts_ns=ts, symbol=symbol, quote=quote, trade=trade))
        # Jittered arrival
        jitter = int(rng.integers(0, tick_interval_ns // 2))
        ts += tick_interval_ns + jitter

    return ticks


def estimate_microprice(quote: Quote) -> float:
    """Size-weighted microprice — useful scalp signal feature."""
    denom = quote.bid_size + quote.ask_size
    if denom <= 0:
        return quote.mid
    return (quote.ask * quote.bid_size + quote.bid * quote.ask_size) / denom


def signed_trade_imbalance(prices: List[float], mids: List[float], sizes: List[int]) -> float:
    """Simple signed volume imbalance vs mid."""
    if not prices:
        return 0.0
    signed = 0.0
    for p, m, s in zip(prices, mids, sizes):
        if p > m:
            signed += s
        elif p < m:
            signed -= s
    total = sum(sizes) or 1
    return signed / total
