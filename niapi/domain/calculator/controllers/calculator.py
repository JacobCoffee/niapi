"""Calculator Controller."""
from __future__ import annotations

from litestar import Controller

__all__ = ["CalculatorController"]


class CalculatorController(Controller):
    """Calculator Controller."""

    opt = {"exclude_from_auth": True}
