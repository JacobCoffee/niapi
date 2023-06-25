"""NIAPI Module."""
from __future__ import annotations

from rich import get_console
from rich.traceback import install as rich_tracebacks

from niapi import asgi, cli
from niapi.metadata import __version__

__all__ = (
    "__version__",
    "asgi",
    "cli",
    "domain",
    "lib",
)

rich_tracebacks(
    console=get_console(),
    suppress=(
        "sqlalchemy",
        "click",
        "rich",
        "saq",
        "litestar",
        "rich_click",
    ),
    show_locals=False,
)
"""Pre-configured traceback handler.

Suppresses some of the frames by default to reduce the amount printed to
the screen.
"""
