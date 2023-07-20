"""NIAPI Domain URLs."""
from __future__ import annotations

from typing import Final

# --- System

INDEX: Final = "/"
"""Index URL."""
SITE_ROOT: Final = "/{path:str}"
"""Site root URL."""
OPENAPI_SCHEMA: Final = "/api"
"""OpenAPI schema URL."""
SYSTEM_HEALTH: Final = "/health"
"""System health URL."""

# --- API
CALCULATOR: Final = "/calculator"
"""Root Calculator Domain URL."""
IP: Final = f"{CALCULATOR}/ip"
"""IP Calculator URL."""
