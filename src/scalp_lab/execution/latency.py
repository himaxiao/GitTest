from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol

import numpy as np


class LatencyModel(Protocol):
    def delay_ns(self, ts_ns: int) -> int:
        """Return additional latency in nanoseconds before order is active."""
        ...


@dataclass(slots=True)
class FixedLatency:
    """Constant one-way latency (signal → exchange)."""

    ms: float = 5.0

    def delay_ns(self, ts_ns: int) -> int:
        return int(self.ms * 1_000_000)


@dataclass(slots=True)
class JitterLatency:
    """Fixed base + uniform jitter — models collocated vs retail path."""

    base_ms: float = 3.0
    jitter_ms: float = 4.0
    seed: int = 7
    _rng: Any = field(default=None, init=False, repr=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "_rng", np.random.default_rng(self.seed))

    def delay_ns(self, ts_ns: int) -> int:
        j = float(self._rng.uniform(0.0, self.jitter_ms))
        return int((self.base_ms + j) * 1_000_000)


@dataclass(slots=True)
class ZeroLatency:
    def delay_ns(self, ts_ns: int) -> int:
        return 0
