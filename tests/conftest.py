"""Testing config."""

from __future__ import annotations

import asyncio
import re
from typing import TYPE_CHECKING

import pytest
from litestar.testing import TestClient
from structlog.contextvars import clear_contextvars
from structlog.testing import CapturingLogger

if TYPE_CHECKING:
    from collections import abc
    from collections.abc import Generator

    from litestar import Litestar
    from pytest import FixtureRequest, MonkeyPatch


@pytest.fixture(scope="session")
def event_loop() -> abc.Iterator[asyncio.AbstractEventLoop]:
    """Scoped Event loop.

    Need the event loop scoped to the session so that we can use it to check
    containers are ready in session scoped containers fixture.

    Returns:
        An event loop.
    """
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    try:
        yield loop
    finally:
        loop.close()


def pytest_addoption(parser: pytest.Parser) -> None:
    """Adds Pytest ini config variables for the plugin.

    Args:
        parser: Pytest fixture.

    Returns:
        None
    """
    parser.addini(
        "unit_test_pattern",
        (
            "Regex used to identify if a test is running as part of a unit or integration test "
            "suite. The pattern is matched against the path of each test function and affects the "
            "behavior of fixtures that are shared between unit and integration tests."
        ),
        type="string",
        default=r"^.*/tests/unit/.*$",
    )


@pytest.fixture(name="app")
def fx_app(pytestconfig: pytest.Config, monkeypatch: MonkeyPatch) -> Litestar:
    """Application fixture.

    Args:
        pytestconfig: Pytest fixture.
        monkeypatch: Pytest fixture.

    Returns:
        The application instance.
    """
    from niapi.asgi import create_app

    return create_app()


@pytest.fixture(name="client")
def fx_client(app: Litestar) -> Generator[TestClient, None, None]:
    """Test client fixture for making calls on the global app instance.

    Args:
        app: The application instance.

    Returns:
        A test client.
    """
    with TestClient(app=app) as client:
        yield client


@pytest.fixture(name="is_unit_test")
def fx_is_unit_test(request: FixtureRequest) -> bool:
    """Uses the ini option `unit_test_pattern` to determine if the test is part
    of unit or integration tests.

    Args:
        request: Pytest fixture.

    Returns:
        True if the test is part of the unit test suite.
    """
    unittest_pattern: str = request.config.getini("unit_test_pattern")  # pyright:ignore
    return bool(re.search(unittest_pattern, str(request.path)))


@pytest.fixture(name="cap_logger")
def fx_cap_logger(monkeypatch: MonkeyPatch) -> CapturingLogger:
    """Used to monkeypatch the app logger, so we can inspect output.

    Args:
        monkeypatch: Pytest fixture.

    Returns:
        CapturingLogger: A logger that captures output.
    """
    import niapi.lib

    niapi.lib.log.configure(
        niapi.lib.log.default_processors  # type:ignore[arg-type]
    )
    clear_contextvars()
    logger = niapi.lib.log.controller.LOGGER.bind()
    logger._logger = CapturingLogger()
    logger._processors = niapi.lib.log.default_processors[:-1]
    monkeypatch.setattr(niapi.lib.log.controller, "LOGGER", logger)
    # noinspection PyProtectedMember
    return logger._logger
