"""Metadata for the Network Information API."""
from __future__ import annotations

import importlib.metadata

__all__ = ["__version__", "__project__"]

__version__ = importlib.metadata.version("niapi")
"""Version of theNetwork Information API package."""
__project__ = importlib.metadata.metadata("niapi")["Name"]
"""Name of the Network Information API package."""
