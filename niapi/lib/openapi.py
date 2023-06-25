"""NIAPI OpenAPI Config."""
from __future__ import annotations

from litestar.openapi.config import OpenAPIConfig
from litestar.openapi.controller import OpenAPIController
from litestar.openapi.spec import Contact

from niapi.lib import settings

__all__ = ("OverridenController",)


class OverridenController(OpenAPIController):
    """Override the default OpenAPIController to use the configured path.

    This is a workaround until `<https://github.com/litestar-org/litestar/issues/1486>`_ is implemented.
    """

    path: str = settings.openapi.PATH


config = OpenAPIConfig(
    title=settings.openapi.TITLE or settings.app.NAME,
    description=settings.openapi.DESCRIPTION,
    servers=settings.openapi.SERVERS,  # type: ignore[arg-type]
    external_docs=settings.openapi.EXTERNAL_DOCS,  # type: ignore[arg-type]
    version=settings.openapi.VERSION,
    contact=Contact(name=settings.openapi.CONTACT_NAME, email=settings.openapi.CONTACT_EMAIL),
    use_handler_docstrings=True,
    root_schema_site="swagger",
    openapi_controller=OverridenController,
)
"""
OpenAPI config for Network Information API.
See :class:`OpenAPISettings <.settings.OpenAPISettings>` for configuration.
"""
