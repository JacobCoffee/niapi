"""Test app/cli.py."""
from collections.abc import Generator
from typing import Any
from unittest.mock import MagicMock, patch

import pytest
from click.testing import CliRunner

from app.cli import _convert_uvicorn_args, run_all_app


def test_convert_uvicorn_args() -> None:
    """Test _convert_uvicorn_args."""
    args = {
        "reload": True,
        "host": "localhost",
        "port": 8000,
        "workers": 2,
        "factory": True,
        "loop": "uvloop",
        "no-access-log": True,
        "timeout-keep-alive": 5,
    }
    expected_result = [
        "--reload",
        "--host=localhost",
        "--port=8000",
        "--workers=2",
        "--factory",
        "--loop=uvloop",
        "--no-access-log",
        "--timeout-keep-alive=5",
    ]
    assert _convert_uvicorn_args(args) == expected_result


@patch("app.cli.multiprocessing.active_children", MagicMock(return_value=[]))
@patch("app.cli.subprocess.run")
def test_run_all_app(mocked_subprocess_run: MagicMock) -> None:
    """Test run_all_app.

    Args:
        mocked_subprocess_run: The mocked subprocess.run function.

    Returns:
        None
    """
    runner = CliRunner()
    result = runner.invoke(run_all_app, ["--host=localhost", "-p8000", "--http-workers=2"])
    assert result.exit_code == 0
    mocked_subprocess_run.assert_called()


@pytest.fixture
def cli_runner() -> Generator[CliRunner, None, None]:
    """Fixture for invoking CLI commands.

    Yields:
        CliRunner: The cli runner.
    """
    yield CliRunner()


def test_run_server(cli_runner: Any, monkeypatch: pytest.MonkeyPatch) -> None:
    """Test the run_server command.

    Args:
        cli_runner: The cli runner.
        monkeypatch: The pytest monkeypatch fixture.

    Returns:
        None
    """
    import app.cli

    run_server_subprocess = MagicMock()
    monkeypatch.setattr(app.cli, "run_all_app", run_server_subprocess)
    result = cli_runner.invoke(app.cli.run_all_app)
    assert result.exit_code == 0
