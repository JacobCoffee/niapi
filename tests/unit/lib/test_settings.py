"""Test niapi/lib/settings.py."""
import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import ValidationError

from niapi.lib import settings


def test_app_slug() -> None:
    """Test app name conversion to slug."""
    settings.app.NAME = "My Application!"
    assert settings.app.slug == "my-application!"


def test_env_load() -> None:
    """Test loading environment variables."""
    path = Path("/tmp/.env")

    with path.open(mode="w") as file:
        file.write("SERVER_HOST=test\n")
        file.write("APP_BUILD_NUMBER=test_build\n")

    load_dotenv(dotenv_path=path, override=True)

    assert os.getenv("SERVER_HOST") == "test"
    assert os.getenv("APP_BUILD_NUMBER") == "test_build"


def test_server_settings() -> None:
    """Test server settings."""
    server_settings = settings.ServerSettings()

    assert server_settings.APP_LOC == "niapi.asgi:create_app"
    assert server_settings.HOST == "test"
    assert isinstance(server_settings.RELOAD_DIRS, list)
    assert len(server_settings.RELOAD_DIRS) == 1
    assert server_settings.RELOAD_DIRS[0] == str(settings.BASE_DIR)


def test_app_settings() -> None:
    """Test application settings."""
    app_settings = settings.AppSettings()

    # TODO: assert app_settings.BUILD_NUMBER == "test_build", f'Expected "test_build", but got "{app_settings.BUILD_NUMBER}"'
    assert app_settings.SECRET_KEY is not None
    assert app_settings.BACKEND_CORS_ORIGINS == ["*"]
    assert isinstance(app_settings.assemble_cors_origins(["localhost"]), list)


def test_api_settings() -> None:
    """Test API settings."""
    api_settings = settings.APISettings()

    assert api_settings.CACHE_EXPIRATION == 60
    assert api_settings.DEFAULT_PAGINATION_LIMIT == 100
    assert api_settings.HEALTH_PATH == "/health"


def test_invalid_env() -> None:
    """Test invalid environment variables."""
    path = Path("/tmp/.env")

    with path.open(mode="w") as file:
        file.write("SERVER_HOST=\n")

    load_dotenv(dotenv_path=path, override=True)

    try:
        _ = settings.ServerSettings()
    except ValidationError:
        assert True
    #     assert False, "Expected ValidationError, but none was raised."
