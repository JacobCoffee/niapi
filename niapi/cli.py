"""NIAPI CLI."""
from __future__ import annotations

import multiprocessing
import subprocess
import sys
from typing import Any

import click
from rich import get_console

from niapi.lib import log, settings

__all__ = [
    "run_all_app",
    "run_app",
]

console = get_console()
"""Pre-configured CLI Console."""

logger = log.get_logger()


@click.group(name="serve", invoke_without_command=False, help="Run application services.")
@click.pass_context
def run_app(_: dict[str, Any]) -> None:
    """Launch Application Components."""


@click.group(name="run-all", invoke_without_command=True, help="Starts the application server.")
@click.option(
    "--host",
    help="Host interface to listen on.  Use 0.0.0.0 for all available interfaces.",
    type=click.STRING,
    default=settings.server.HOST,
    required=False,
    show_default=True,
)
@click.option(
    "-p",
    "--port",
    help="Port to bind.",
    type=click.INT,
    default=settings.server.PORT,
    required=False,
    show_default=True,
)
@click.option(
    "--http-workers",
    help="The number of HTTP worker processes for handling requests.",
    type=click.IntRange(min=1, max=multiprocessing.cpu_count() + 1),
    default=multiprocessing.cpu_count() + 1,
    required=False,
    show_default=True,
)
@click.option("-r", "--reload", help="Enable reload", is_flag=True, default=False, type=bool)
@click.option("-v", "--verbose", help="Enable verbose logging.", is_flag=True, default=False, type=bool)
@click.option("-d", "--debug", help="Enable debugging.", is_flag=True, default=False, type=bool)
def run_all_app(
    host: str,
    port: int | None,
    http_workers: int | None,
    reload: bool | None,
    verbose: bool | None,
    debug: bool | None,
) -> None:
    """Run the API server."""
    log.config.configure()
    settings.server.HOST = host or settings.server.HOST
    settings.server.PORT = port or settings.server.PORT
    settings.server.RELOAD = reload or settings.server.RELOAD if settings.server.RELOAD is not None else None
    settings.server.HTTP_WORKERS = http_workers or settings.server.HTTP_WORKERS
    settings.app.DEBUG = debug or settings.app.DEBUG
    settings.log.LEVEL = 10 if verbose or settings.app.DEBUG else settings.log.LEVEL
    logger.info("starting all application services.")

    try:
        logger.info("Starting HTTP Server.")
        reload_dirs = settings.server.RELOAD_DIRS if settings.server.RELOAD else None
        process_args = {
            "reload": bool(settings.server.RELOAD),
            "host": settings.server.HOST,
            "port": settings.server.PORT,
            "workers": 1 if bool(settings.server.RELOAD or settings.app.DEV_MODE) else settings.server.HTTP_WORKERS,
            "factory": settings.server.APP_LOC_IS_FACTORY,
            "loop": "uvloop",
            "no-access-log": True,
            "timeout-keep-alive": settings.server.KEEPALIVE,
        }
        if reload_dirs:
            process_args["reload-dir"] = reload_dirs
        subprocess.run(
            ["uvicorn", settings.server.APP_LOC, *_convert_uvicorn_args(process_args)], check=True  # noqa: S603, S607
        )
    finally:
        for process in multiprocessing.active_children():
            process.terminate()
        logger.info("⏏️  Shutdown complete")
        sys.exit()


def _convert_uvicorn_args(args: dict[str, Any]) -> list[str]:
    process_args: list[str] = []
    for arg, value in args.items():
        if isinstance(value, list):
            process_args.extend(f"--{arg}={val}" for val in value)
        if isinstance(value, bool):
            if value:
                process_args.append(f"--{arg}")
        else:
            process_args.append(f"--{arg}={value}")

    return process_args
