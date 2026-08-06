from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional

from scalp_lab.data.tick import Tick
from scalp_lab.engine.events import SignalEvent
from scalp_lab.execution.order import Fill
from scalp_lab.portfolio.account import Account


class Strategy(ABC):
    """Strategy sees ticks and optional fills; emits signals only.

    No direct order placement — keeps research code testable and
    execution realism centralized in the fill simulator.
    """

    def __init__(self, symbol: str) -> None:
        self.symbol = symbol
        self.account: Optional[Account] = None

    def bind_account(self, account: Account) -> None:
        self.account = account

    @abstractmethod
    def on_tick(self, tick: Tick) -> List[SignalEvent]:
        ...

    def on_fill(self, fill: Fill) -> None:
        """Optional fill callback for stateful strategies."""
        return None
