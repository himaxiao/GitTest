"""Unit tests for core fill / engine / calibrator paths."""

from __future__ import annotations

from scalp_lab.data.synthetic import generate_synthetic_ticks
from scalp_lab.data.tick import Quote, Side, Tick
from scalp_lab.engine.engine import BacktestEngine, EngineConfig
from scalp_lab.execution.fills import BidAskFillSimulator
from scalp_lab.execution.latency import FixedLatency, ZeroLatency
from scalp_lab.execution.order import Fill, Order, OrderStatus, OrderType
from scalp_lab.execution.slippage import FixedBpsSlippage, ZeroSlippage
from scalp_lab.live.calibrator import LiveCalibrator
from scalp_lab.metrics.report import compute_report
from scalp_lab.paper.broker import PaperBroker
from scalp_lab.strategy.microprice_scalp import MicropriceScalp


def test_market_buy_crosses_ask():
    sim = BidAskFillSimulator(latency=ZeroLatency(), slippage=ZeroSlippage())
    order = Order(
        symbol="AAPL",
        side=Side.BUY,
        qty=100,
        order_type=OrderType.MARKET,
        created_ts_ns=1_000,
    )
    sim.submit(order)
    tick = Tick(
        ts_ns=1_000,
        symbol="AAPL",
        quote=Quote(
            ts_ns=1_000, symbol="AAPL", bid=100.0, ask=100.02, bid_size=500, ask_size=500
        ),
    )
    fills = sim.on_tick(tick)
    assert len(fills) == 1
    assert fills[0].price == 100.02
    assert order.status == OrderStatus.FILLED


def test_latency_delays_fill():
    sim = BidAskFillSimulator(latency=FixedLatency(ms=10), slippage=ZeroSlippage())
    order = Order(
        symbol="AAPL",
        side=Side.SELL,
        qty=100,
        order_type=OrderType.MARKET,
        created_ts_ns=0,
    )
    sim.submit(order)
    early = Tick(
        ts_ns=5_000_000,
        symbol="AAPL",
        quote=Quote(
            ts_ns=5_000_000,
            symbol="AAPL",
            bid=99.99,
            ask=100.01,
            bid_size=100,
            ask_size=100,
        ),
    )
    assert sim.on_tick(early) == []
    later = Tick(
        ts_ns=11_000_000,
        symbol="AAPL",
        quote=Quote(
            ts_ns=11_000_000,
            symbol="AAPL",
            bid=99.99,
            ask=100.01,
            bid_size=100,
            ask_size=100,
        ),
    )
    fills = sim.on_tick(later)
    assert len(fills) == 1
    assert fills[0].price == 99.99
    assert fills[0].latency_ns == 10_000_000


def test_limit_not_filled_through_book():
    sim = BidAskFillSimulator(latency=ZeroLatency(), slippage=ZeroSlippage())
    order = Order(
        symbol="AAPL",
        side=Side.BUY,
        qty=100,
        order_type=OrderType.LIMIT,
        limit_price=99.90,
        created_ts_ns=0,
    )
    sim.submit(order)
    tick = Tick(
        ts_ns=1,
        symbol="AAPL",
        quote=Quote(
            ts_ns=1, symbol="AAPL", bid=100.0, ask=100.02, bid_size=100, ask_size=100
        ),
    )
    assert sim.on_tick(tick) == []


def test_end_to_end_synthetic_backtest():
    ticks = generate_synthetic_ticks(n_ticks=2000, seed=1)
    strategy = MicropriceScalp(symbol="AAPL", entry_z=1.0, max_hold_ticks=20)
    engine = BacktestEngine(
        strategy=strategy,
        config=EngineConfig(
            latency=FixedLatency(ms=2),
            slippage=FixedBpsSlippage(bps=1.0),
        ),
    )
    result = engine.run(ticks)
    report = compute_report(result.account)
    assert result.signals >= 0
    assert report.n_fills == result.fills
    assert len(result.account.equity_curve) > 0


def test_paper_broker_market_fill():
    broker = PaperBroker()
    q = Quote(ts_ns=10, symbol="MSFT", bid=400.0, ask=400.05, bid_size=200, ask_size=200)
    broker.on_quote(q)
    order = broker.submit_market("MSFT", Side.BUY, 100, ts_ns=11)
    assert order.status == OrderStatus.FILLED
    assert broker.account.position("MSFT").qty == 100


def test_live_calibrator_gap():
    cal = LiveCalibrator()
    cal.add_backtest(
        [
            Fill(
                order_id="1",
                symbol="AAPL",
                side=Side.BUY,
                qty=100,
                price=100.01,
                ts_ns=1,
                slippage=0.01,
            )
        ]
    )
    cal.add_live(
        [
            Fill(
                order_id="2",
                symbol="AAPL",
                side=Side.BUY,
                qty=100,
                price=100.03,
                ts_ns=2,
                slippage=0.03,
            )
        ]
    )
    r = cal.report()
    assert abs(r["slippage_gap"] - 0.02) < 1e-9
