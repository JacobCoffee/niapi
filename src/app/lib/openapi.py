"""NIAPI OpenAPI Config."""

from __future__ import annotations

from litestar.openapi.config import OpenAPIConfig
from litestar.openapi.plugins import RedocRenderPlugin, ScalarRenderPlugin, StoplightRenderPlugin, SwaggerRenderPlugin
from litestar.openapi.spec import Contact

from app.lib import settings

__all__ = ("config",)

config = OpenAPIConfig(
    title=settings.openapi.TITLE or settings.app.NAME,
    version=settings.openapi.VERSION,
    contact=Contact(name=settings.openapi.CONTACT_NAME, email=settings.openapi.CONTACT_EMAIL),
    use_handler_docstrings=True,
    path=settings.openapi.PATH,
    servers=settings.openapi.SERVERS,  # type: ignore[arg-type]
    external_docs=settings.openapi.EXTERNAL_DOCS,  # type: ignore[arg-type]
    create_examples=True,
    render_plugins=[
        ScalarRenderPlugin(version="1.20.7", path="/", css_url="/static/scalar_api.css"),
        SwaggerRenderPlugin(),
        StoplightRenderPlugin(),
        RedocRenderPlugin(),
    ],
)
"""
OpenAPI config for Network Information API.
See :class:`OpenAPISettings <.settings.OpenAPISettings>` for configuration.
"""
