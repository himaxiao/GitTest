from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

import numpy as np
import pandas as pd

from scalp_lab.portfolio.account import Account


@dataclass
class PerformanceReport:
    n_fills: int
    n_trades: int  # round-trips approx
    total_fees: float
    realized_pnl: float
    final_equity: float
    total_return: float
    max_drawdown: float
    sharpe_approx: float
    avg_slippage: float
    avg_latency_ms: float

    def to_dict(self) -> dict:
        return self.__dict__.copy()

    def summary(self) -> str:
        return (
            f"fills={self.n_fills} realized_pnl={self.realized_pnl:.2f} "
            f"equity={self.final_equity:.2f} ret={self.total_return:.4%} "
            f"mdd={self.max_drawdown:.4%} sharpe~={self.sharpe_approx:.2f} "
            f"avg_slip={self.avg_slippage:.4f} avg_lat_ms={self.avg_latency_ms:.2f} "
            f"fees={self.total_fees:.2f}"
        )


def compute_report(account: Account, initial_cash: float = 100_000.0) -> PerformanceReport:
    fills = account.fills
    equity = account.equity_curve
    eq_vals = np.array([e for _, e in equity], dtype=float) if equity else np.array([initial_cash])

    # Drawdown
    peak = np.maximum.accumulate(eq_vals)
    dd = (eq_vals - peak) / np.where(peak == 0, 1, peak)
    max_dd = float(dd.min()) if len(dd) else 0.0

    # Approx sharpe on equity diffs (not annualized rigorously for ticks)
    diffs = np.diff(eq_vals)
    if len(diffs) > 2 and diffs.std() > 1e-12:
        sharpe = float(diffs.mean() / diffs.std() * np.sqrt(len(diffs)))
    else:
        sharpe = 0.0

    avg_slip = float(np.mean([f.slippage for f in fills])) if fills else 0.0
    avg_lat = float(np.mean([f.latency_ns for f in fills]) / 1_000_000) if fills else 0.0

    final_eq = float(eq_vals[-1]) if len(eq_vals) else account.equity()
    return PerformanceReport(
        n_fills=len(fills),
        n_trades=len(fills) // 2,
        total_fees=account.fees_paid,
        realized_pnl=account.realized_pnl,
        final_equity=final_eq,
        total_return=(final_eq - initial_cash) / initial_cash,
        max_drawdown=max_dd,
        sharpe_approx=sharpe,
        avg_slippage=avg_slip,
        avg_latency_ms=avg_lat,
    )


def fills_to_frame(account: Account) -> pd.DataFrame:
    rows = []
    for f in account.fills:
        rows.append(
            {
                "ts_ns": f.ts_ns,
                "symbol": f.symbol,
                "side": f.side.value,
                "qty": f.qty,
                "price": f.price,
                "fee": f.fee,
                "slippage": f.slippage,
                "latency_ms": f.latency_ns / 1_000_000,
                "reason": f.reason,
            }
        )
    return pd.DataFrame(rows)
