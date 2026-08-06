from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

import numpy as np

from scalp_lab.execution.order import Fill


@dataclass
class LiveCalibrator:
    """Compare backtest fill assumptions vs paper/live fills.

    Use after a paper-trading session to tighten latency/slippage params.
    """

    bt_fills: List[Fill] = field(default_factory=list)
    live_fills: List[Fill] = field(default_factory=list)

    def add_backtest(self, fills: List[Fill]) -> None:
        self.bt_fills.extend(fills)

    def add_live(self, fills: List[Fill]) -> None:
        self.live_fills.extend(fills)

    def report(self) -> Dict[str, float]:
        def avg_slip(fills: List[Fill]) -> float:
            if not fills:
                return float("nan")
            return float(np.mean([f.slippage for f in fills]))

        def avg_lat_ms(fills: List[Fill]) -> float:
            if not fills:
                return float("nan")
            return float(np.mean([f.latency_ns for f in fills]) / 1_000_000)

        def avg_fee(fills: List[Fill]) -> float:
            if not fills:
                return float("nan")
            return float(np.mean([f.fee for f in fills]))

        bt_slip = avg_slip(self.bt_fills)
        live_slip = avg_slip(self.live_fills)
        bt_lat = avg_lat_ms(self.bt_fills)
        live_lat = avg_lat_ms(self.live_fills)

        return {
            "bt_avg_slippage": bt_slip,
            "live_avg_slippage": live_slip,
            "slippage_gap": live_slip - bt_slip if np.isfinite(live_slip) and np.isfinite(bt_slip) else float("nan"),
            "bt_avg_latency_ms": bt_lat,
            "live_avg_latency_ms": live_lat,
            "latency_gap_ms": live_lat - bt_lat if np.isfinite(live_lat) and np.isfinite(bt_lat) else float("nan"),
            "bt_avg_fee": avg_fee(self.bt_fills),
            "live_avg_fee": avg_fee(self.live_fills),
            "n_bt_fills": float(len(self.bt_fills)),
            "n_live_fills": float(len(self.live_fills)),
        }

    def suggested_slippage_bps(self, base_bps: float = 0.5) -> float:
        """Heuristic: bump backtest bps by observed live gap."""
        r = self.report()
        gap = r["slippage_gap"]
        if not np.isfinite(gap):
            return base_bps
        # Convert absolute $ gap roughly via last mid if available — else scale bps up
        bump = max(0.0, gap) * 10_000  # crude if slippage stored in $
        return float(base_bps + min(bump, 20.0))
