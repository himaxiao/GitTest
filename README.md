# Scalp Lab

Tick-level event-driven research framework for **US equity scalping**.

Built for the path:

```
Tick data → Event-driven backtest → Bid/Ask fill sim → Slippage & latency
        → Paper trading → Small-capital live calibration
```

OHLC / Pine-style bar backtests systematically overstate scalp edge (ignored
queue position, spread crossing, delay). This lab keeps execution realism in
the engine so strategy code stays thin and comparable to live.

## Why not TradingView first?

TradingView + Pine is excellent for *idea screening* on bars. For holds of
tens of seconds to a few minutes, fill quality dominates alpha. Move signal
prototypes here once you care about:

- NBBO bid/ask (not bar close)
- Latency between signal and exchange
- Partial fills vs displayed size
- Slippage / fee drag
- Paper vs backtest gap (calibration loop)

## Layout

```
src/scalp_lab/
  data/        Tick / Quote / Trade, parquet store, synthetic generator
  engine/      Event types + BacktestEngine
  execution/   Orders, bid/ask fills, slippage & latency models
  strategy/    Strategy ABC + example MicropriceScalp
  portfolio/   Account / position / mark-to-market
  metrics/     PnL, drawdown, slippage/latency stats
  paper/       PaperBroker (same Account model)
  live/        LiveCalibrator (tighten model from paper/live fills)
  examples/    End-to-end demo
```

## Quick start

```bash
pip install -e ".[dev]"
pytest
python -m scalp_lab.examples.run_backtest --ticks 5000
```

## Roadmap (next increments)

1. **Real tick ingest** — Polygon / Databento / Interactive Brokers NBBO → `TickStore`
2. **Queue / L2** — optional depth beyond top-of-book for limit scalps
3. **Broker adapters** — IBKR / Alpaca paper session behind `PaperBroker`
4. **Live calibrator job** — nightly compare BT vs paper fills → update bps/ms
5. **Small capital** — same strategy object, live risk caps, kill switch

Pine stays useful for visual confirmation; this repo owns research → automation.
