"""Application Modules."""
from __future__ import annotations

from typing import TYPE_CHECKING

from litestar.contrib.repository.filters import FilterTypes
from litestar.pagination import OffsetPagination
from pydantic import EmailStr

from . import system, urls, web

if TYPE_CHECKING:
    from collections.abc import Mapping
    from typing import Any

    from litestar.types import ControllerRouterHandler

__all__ = [
    "system",
    "web",
    "urls",
    "routes",
    "signature_namespace",
]

routes: list[ControllerRouterHandler] = [
    # system.controllers.system.SystemController,
    web.controllers.web.WebController,
]
"""Routes for the application."""

signature_namespace: Mapping[str, Any] = {
    "FilterTypes": FilterTypes,
    "EmailStr": EmailStr,
    "OffsetPagination": OffsetPagination,
}
"""Namespace for the application signature."""
