"""NIAPI Static files configuration."""
from __future__ import annotations

from pathlib import Path

from litestar.static_files.config import StaticFilesConfig

from . import settings

STATIC_DIRS = [settings.app.STATIC_DIR]
if settings.app.DEBUG:
    STATIC_DIRS.append(Path(settings.BASE_DIR / "domain" / "web" / "resources"))

config = [
    StaticFilesConfig(
        directories=STATIC_DIRS,  # type: ignore[arg-type]
        path=settings.app.STATIC_URL,
        name="web",
        html_mode=True,
        opt={"exclude_from_auth": True},
    ),
]
"""
Network Information API Static files configuration. See :class:`OpenAPISettings <.settings.OpenAPISettings>` and
general :mod:`Settings.py <.settings>` for configuration.
"""
