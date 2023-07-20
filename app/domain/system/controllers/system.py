"""System Controller."""
from __future__ import annotations

from litestar import Controller

__all__ = ["SystemController"]


class SystemController(Controller):
    """System Controller."""

    opt = {"exclude_from_auth": True}
