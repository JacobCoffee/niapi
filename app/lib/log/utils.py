"""Logging utilities.

:func:`msgspec_json_renderer()` - A JSON Renderer for structlog using msgspec.

Msgspec doesn't have an API consistent with the stdlib's :mod:`json` module,
which is required for :class:`Structlog's JSONRenderer <structlog.processors.JSONRenderer>`.

:class:`EventFilter` - A structlog processor that removes keys from the log event if they exist.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

__all__ = ["EventFilter", "msgspec_json_renderer"]

from app.lib import serialization

if TYPE_CHECKING:
    from collections.abc import Iterable

    from structlog.typing import EventDict, WrappedLogger


def msgspec_json_renderer(_: WrappedLogger, __: str, event_dict: EventDict) -> bytes:
    """Structlog processor that uses :doc:`msgspec <msgspec:index>` for JSON encoding.

    Args:
        _:
        __:
        event_dict: The data to be logged.

    Returns:
        The log event encoded to JSON by msgspec.
    """
    return serialization.to_json(event_dict)


class EventFilter:
    """Remove keys from the log event.

    Add an instance to the processor chain.

    Example:
    # noqa

    .. code-block:: python

        structlog.configure(
            ...,
            processors=[
                ...,
                EventFilter(["color_message"]),
                ...,
            ],
        )

    """

    def __init__(self, filter_keys: Iterable[str]) -> None:
        """Initialize the processor.

        Args:
            filter_keys: Iterable of string keys to be excluded from the log event.

        Returns:
            None
        """
        self.filter_keys = filter_keys

    def __call__(self, _: WrappedLogger, __: str, event_dict: EventDict) -> EventDict:
        """Receive the log event, and filter keys.

        Args:
            _:
            __:
            event_dict: The data to be logged.

        Returns:
            The log event with any key in ``self.filter_keys`` removed.
        """
        for key in self.filter_keys:
            event_dict.pop(key, None)
        return event_dict
