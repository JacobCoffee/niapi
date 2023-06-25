"""NIAPI settings."""
from __future__ import annotations

import binascii
import os
from pathlib import Path
from typing import Final

from dotenv import load_dotenv
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.data_extractors import RequestExtractorField, ResponseExtractorField  # noqa: TCH002
from pydantic import BaseSettings, SecretBytes, ValidationError, validator

from niapi import utils
from niapi.metadata import __version__ as version

__all__ = (
    "APISettings",
    "AppSettings",
    "HTTPClientSettings",
    "LogSettings",
    "OpenAPISettings",
    "ServerSettings",
    "TemplateSettings",
    "load_settings",
)


load_dotenv()

DEFAULT_MODULE_NAME = "niapi"
BASE_DIR: Final = utils.module_to_os_path(DEFAULT_MODULE_NAME)
STATIC_DIR = Path(BASE_DIR / "domain" / "web" / "public")
TEMPLATES_DIR = Path(BASE_DIR / "domain" / "web" / "templates")


class ServerSettings(BaseSettings):
    """Server configurations."""

    class Config:
        """Pydantic Config.

        .. note:: See https://docs.pydantic.dev/usage/settings/#settings-configuration

        """

        case_sensitive = True
        env_file = ".env"
        env_prefix = "SERVER_"

    APP_LOC: str = "niapi.asgi:create_app"
    """Path to app executable, or factory."""
    APP_LOC_IS_FACTORY: bool = True
    """Indicate if APP_LOC points to an executable or factory."""
    HOST: str = "localhost"
    """Server network host."""
    KEEPALIVE: int = 65
    """Seconds to hold connections open."""
    PORT: int = 8000
    """Server port."""
    RELOAD: bool = False
    """Turn on hot reloading."""
    RELOAD_DIRS: list[str] = [f"{BASE_DIR}"]
    """Directories to watch for reloading.

    .. warning:: This only accepts a single directory for now, something is broken

    """
    HTTP_WORKERS: int | None = None
    """Number of HTTP Worker processes to be spawned by Uvicorn."""


class AppSettings(BaseSettings):
    """Generic application settings.

    These settings are returned as JSON by the healthcheck endpoint, so
    do not include any sensitive values here, or if you do ensure to
    exclude them from serialization in the ``Config`` object.
    """

    class Config:
        """App settings config."""

        case_sensitive = True
        env_file = ".env"

    BUILD_NUMBER: str = ""
    """Identifier for CI build."""
    CHECK_DB_READY: bool = True
    """Check for database readiness on startup."""
    CHECK_REDIS_READY: bool = True
    """Check for redis readiness on startup."""
    DEBUG: bool = False
    """Run ``Litestar`` with ``debug=True``."""
    ENVIRONMENT: str = "prod"
    """``dev``, ``prod``, ``qa``, etc."""
    TEST_ENVIRONMENT_NAME: str = "test"
    """Value of ENVIRONMENT used to determine if running tests.

    This should be the value of ``ENVIRONMENT`` in ``tests.env``.
    """
    LOCAL_ENVIRONMENT_NAME: str = "local"
    """Value of ENVIRONMENT used to determine if running in local development
    mode.

    This should be the value of ``ENVIRONMENT`` in your local ``.env`` file.
    """
    NAME: str = "Network Information API"
    """Application name."""
    SECRET_KEY: SecretBytes
    """Secret key used for signing cookies and other things."""
    JWT_ENCRYPTION_ALGORITHM: str = "HS256"
    """Algorithm used to encrypt JWTs."""
    BACKEND_CORS_ORIGINS: list[str] = ["*"]
    """List of origins allowed to access the API."""
    STATIC_URL: str = "/static/"
    """Default URL where static assets are located."""
    CSRF_COOKIE_NAME: str = "csrftoken"
    """Name of the CSRF cookie."""
    CSRF_COOKIE_SECURE: bool = False
    """Set the CSRF cookie to be secure."""
    STATIC_DIR: Path = STATIC_DIR
    """Path to static assets."""
    DEV_MODE: bool = False
    """Indicate if running in development mode."""

    @property
    def slug(self) -> str:
        """Return a slugified name.

        Returns:
            ``self.NAME``, all lowercase and hyphens instead of spaces.
        """
        return "-".join(s.lower() for s in self.NAME.split())

    @validator("BACKEND_CORS_ORIGINS", pre=True, allow_reuse=True)
    def assemble_cors_origins(
        cls,
        value: str | list[str],
    ) -> list[str] | str:
        """Parse a list of origins.

        Args:
            value: A comma-separated string of origins, or a list of origins.

        Returns:
            A list of origins.

        Raises:
            ValueError: If ``value`` is not a list or string.
        """
        if isinstance(value, list):
            return value
        if isinstance(value, str) and not value.startswith("["):
            return [host.strip() for host in value.split(",")]
        if isinstance(value, str) and value.startswith("[") and value.endswith("]"):
            return list(value)
        raise ValueError(value)

    @validator("SECRET_KEY", pre=True, always=True, allow_reuse=True)
    def generate_secret_key(
        cls,
        value: SecretBytes | None,
    ) -> SecretBytes:
        """Generate a secret key.

        Args:
            value: A secret key, or ``None``.

        Returns:
            A secret key.
        """
        if value is None:
            return SecretBytes(binascii.hexlify(os.urandom(32)))
        return value


class APISettings(BaseSettings):
    """API specific configuration."""

    class Config:
        """API specific configuration."""

        case_sensitive = True
        env_file = ".env"
        env_prefix = "API_"

    CACHE_EXPIRATION: int = 60
    """Default cache key expiration in seconds."""
    DEFAULT_PAGINATION_LIMIT: int = 100
    """Max records received for collection routes."""
    HEALTH_PATH: str = "/health"
    """Route that the health check is served under."""


class LogSettings(BaseSettings):
    """Logging config for the Network Information API."""

    class Config:
        """Logging config for the Network Information API."""

        case_sensitive = True
        env_file = ".env"
        env_prefix = "LOG_"

    """https://stackoverflow.com/a/1845097/6560549"""
    EXCLUDE_PATHS: str = r"\A(?!x)x"
    """Regex to exclude paths from logging."""
    HTTP_EVENT: str = "HTTP"
    """Log event name for logs from ``litestar`` handlers."""
    INCLUDE_COMPRESSED_BODY: bool = False
    """Include ``body`` of compressed responses in log output."""
    LEVEL: int = 20
    """Stdlib log levels.

    Only emit logs at this level, or higher.
    """
    OBFUSCATE_COOKIES: set[str] = {"session"}
    """Request cookie keys to obfuscate."""
    OBFUSCATE_HEADERS: set[str] = {"Authorization", "X-API-KEY"}
    """Request header keys to obfuscate."""
    JOB_FIELDS: list[str] = [
        "function",
        "kwargs",
        "key",
        "scheduled",
        "attempts",
        "completed",
        "queued",
        "started",
        "result",
        "error",
    ]
    """Attributes of the SAQ :class:`Job <saq.job.Job>` to be logged."""
    REQUEST_FIELDS: list[RequestExtractorField] = [
        "path",
        "method",
        "headers",
        "cookies",
        "query",
        "path_params",
        "body",
    ]
    """Attributes of the :class:`Request <litestar.connection.request.Request>` to be
    logged."""
    RESPONSE_FIELDS: list[ResponseExtractorField] = [
        "status_code",
        "cookies",
        "headers",
        # "body",  # ! We don't want to log the response body.
    ]
    """Attributes of the :class:`Response <litestar.response.Response>` to be
    logged."""
    UVICORN_ACCESS_LEVEL: int = 30
    """Level to log uvicorn access logs."""
    UVICORN_ERROR_LEVEL: int = 20
    """Level to log uvicorn error logs."""


# noinspection PyUnresolvedReferences
class OpenAPISettings(BaseSettings):
    """Configures OpenAPI for the Network Information API."""

    class Config:
        """Configures OpenAPI for the Network Information API."""

        case_sensitive = True
        env_file = ".env"
        env_prefix = "OPENAPI_"

    CONTACT_NAME: str = "Admin"
    """Name of contact on document."""
    CONTACT_EMAIL: str = "hello@niapi.app"
    """Email for contact on document."""
    TITLE: str | None = "Network Information API"
    """Document title."""
    VERSION: str = version
    """Document version."""
    PATH: str = "/api"
    """Path to access the root API documentation."""
    DESCRIPTION: str | None = f"""The Network Information API gives you, well... network information!
                                  You can find out more about this project in the
                                  [docs]({os.getenv("NIAPI_URL", "http://localhost") + "docs"})."""
    SERVERS: list[dict[str, str]] = []
    """Servers to use for the OpenAPI documentation."""
    EXTERNAL_DOCS: dict[str, str] | None = {
        "description": "Network Information API Docs",
        "url": os.getenv("NIAPI_URL", "http://localhost") + "docs",
    }
    """External documentation for the API."""

    @validator("SERVERS", pre=True, allow_reuse=True)
    def assemble_openapi_servers(cls, value: list[dict[str, str]]) -> list[dict[str, str]]:
        """Assembles the OpenAPI servers based on the environment.

        Args:
            value: The value of the SERVERS setting.

        Returns:
            The assembled OpenAPI servers.
        """
        environment = os.getenv("ENVIRONMENT")

        if environment == "prod":
            return [
                {
                    "url": os.getenv("NIAPI_URL", "https://niapi.app/"),
                    "description": "Production",
                },
            ]
        if environment == "dev":
            return [{"url": "http://0.0.0.0:8000", "description": "Local Development"}]

        return value


class TemplateSettings(BaseSettings):
    """Configures Templating for the Network Information API."""

    class Config:
        """Configures Templating for the Network Information API."""

        case_sensitive = True
        env_file = ".env"
        env_prefix = "TEMPLATE_"

    ENGINE: type[JinjaTemplateEngine] = JinjaTemplateEngine
    """Template engine to use. (Jinja2 or Mako)"""


class HTTPClientSettings(BaseSettings):
    """HTTP Client configurations."""

    class Config:
        """HTTP Client configurations."""

        case_sensitive = True
        env_file = ".env"
        env_prefix = "HTTP_"

    BACKOFF_MAX: float = 60
    BACKOFF_MIN: float = 0
    EXPONENTIAL_BACKOFF_BASE: float = 2
    EXPONENTIAL_BACKOFF_MULTIPLIER: float = 1


# noinspection PyShadowingNames
def load_settings() -> (
    tuple[
        AppSettings,
        APISettings,
        OpenAPISettings,
        TemplateSettings,
        ServerSettings,
        LogSettings,
        HTTPClientSettings,
    ]
):
    """Load Settings file.

    As an example, I've commented out how you might go about injecting secrets into the environment for production.
    This fetches a ``.env`` configuration and configures the Network Information API to use it.

    .. todo:: Finish example

    .. code-block:: python

        secret_id = os.environ.get("ENV_SECRETS", None)
        env_file_exists = os.path.isfile(f"{os.curdir}/.env")

        try:
            settings = ...  # existing code below
        except:
            ...
        return settings

    Returns:
        Settings: application settings
    """
    try:
        """Override Application reload dir."""
        server: ServerSettings = ServerSettings.parse_obj(
            {"HOST": "0.0.0.0", "RELOAD_DIRS": [str(BASE_DIR)]},  # noqa: S104
        )
        app: AppSettings = AppSettings.parse_obj({})
        api: APISettings = APISettings.parse_obj({})
        openapi: OpenAPISettings = OpenAPISettings.parse_obj({})
        template: TemplateSettings = TemplateSettings.parse_obj({})
        log: LogSettings = LogSettings.parse_obj({})
        http_client: HTTPClientSettings = HTTPClientSettings.parse_obj({})

    except ValidationError as error:
        print(f"Could not load settings. Error: {error!r}")  # noqa: T201
        raise error from error
    return (
        app,
        api,
        openapi,
        template,
        server,
        log,
        http_client,
    )


(
    app,
    api,
    openapi,
    template,
    server,
    log,
    http_client,
) = load_settings()
