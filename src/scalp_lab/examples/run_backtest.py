"""Run a synthetic-tick backtest end-to-end."""

from __future__ import annotations

import argparse

from scalp_lab.data.synthetic import generate_synthetic_ticks
from scalp_lab.engine.engine import BacktestEngine, EngineConfig
from scalp_lab.execution.latency import JitterLatency
from scalp_lab.execution.slippage import SpreadAwareSlippage
from scalp_lab.metrics.report import compute_report
from scalp_lab.strategy.microprice_scalp import MicropriceScalp


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Scalp Lab synthetic backtest demo")
    parser.add_argument("--symbol", default="AAPL")
    parser.add_argument("--ticks", type=int, default=5000)
    parser.add_argument("--cash", type=float, default=100_000.0)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args(argv)

    ticks = generate_synthetic_ticks(symbol=args.symbol, n_ticks=args.ticks, seed=args.seed)
    strategy = MicropriceScalp(symbol=args.symbol, entry_z=1.2, max_hold_ticks=30)
    config = EngineConfig(
        initial_cash=args.cash,
        latency=JitterLatency(base_ms=3.0, jitter_ms=5.0, seed=args.seed),
        slippage=SpreadAwareSlippage(extra_spread_frac=0.0, impact_bps_per_displayed=1.5),
    )
    engine = BacktestEngine(strategy=strategy, config=config)
    result = engine.run(ticks)
    report = compute_report(result.account, initial_cash=args.cash)

    print("=== Scalp Lab Demo ===")
    print(f"symbol={args.symbol} ticks={len(ticks)}")
    print(
        f"signals={result.signals} orders={result.orders} fills={result.fills}"
    )
    print(report.summary())
    pos = result.account.position(args.symbol)
    print(f"final_position qty={pos.qty} avg={pos.avg_price:.4f} cash={result.account.cash:.2f}")


if __name__ == "__main__":
    main()
