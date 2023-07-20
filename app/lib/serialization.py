"""NIAPI Serialization Helpers."""
from __future__ import annotations

import datetime
from json import JSONEncoder
from typing import Any
from uuid import UUID

import msgspec
from pydantic import BaseModel

__all__ = [
    "convert_datetime_to_gmt",
    "convert_string_to_camel_case",
    "convert_camel_to_snake_case",
    "from_json",
    "from_msgpack",
    "to_json",
    "to_msgpack",
    "UUIDEncoder",
]


def _default(value: Any) -> str:
    """Default encoder for msgspec.

    Args:
        value: The value to encode

    Returns:
        str: The encoded value
    """
    if isinstance(value, BaseModel):
        return str(value.dict(by_alias=True))
    try:
        val = str(value)
    except Exception as exc:  # noqa: BLE001
        raise TypeError from exc
    else:
        return val


_msgspec_json_encoder = msgspec.json.Encoder(enc_hook=_default)
_msgspec_json_decoder = msgspec.json.Decoder()
_msgspec_msgpack_encoder = msgspec.msgpack.Encoder(enc_hook=_default)
_msgspec_msgpack_decoder = msgspec.msgpack.Decoder()


def to_json(value: Any) -> bytes:
    """Encode json with the optimized :doc:`msgspec <msgspec:index>` package.

    Args:
        value: The value to encode

    Returns:
        bytes: The encoded value
    """
    return _msgspec_json_encoder.encode(value)


def from_json(value: bytes | str) -> Any:
    """Decode to an object with the optimized :doc:`msgspec <msgspec:index>` package.

    Args:
        value: The value to decode

    Returns:
        Any: The decoded value
    """
    return _msgspec_json_decoder.decode(value)


def to_msgpack(value: Any) -> bytes:
    """Encode json with the optimized :doc:`msgspec <msgspec:index>` package.

    Args:
        value: The value to encode

    Returns:
        bytes: The encoded value
    """
    return _msgspec_msgpack_encoder.encode(value)


def from_msgpack(value: bytes) -> Any:
    """Decode to an object with the optimized :doc:`msgspec <msgspec:index>` package.

    Args:
        value: The value to decode

    Returns:
        Any: The decoded value
    """
    return _msgspec_msgpack_decoder.decode(value)


def convert_datetime_to_gmt(dt: datetime.datetime) -> str:
    """Handle datetime serialization for nested timestamps.

    Args:
        dt: The datetime to convert

    Returns:
        str: The datetime converted to GMT
    """
    if not dt.tzinfo:
        dt = dt.replace(tzinfo=datetime.UTC)
    return dt.isoformat().replace("+00:00", "Z")


def convert_string_to_camel_case(string: str) -> str:
    """Convert a string to camel case.

    Args:
        string: The string to convert

    Returns:
        str: The string converted to camel case
    """
    return "".join(word if index == 0 else word.capitalize() for index, word in enumerate(string.split("_")))


def convert_camel_to_snake_case(string: str) -> str:
    """Convert a string to snake case.

    Args:
        string: The string to convert

    Returns:
        str: The string converted to snake case
    """
    return "".join(f"_{char.lower()}" if index > 0 and char.isupper() else char for index, char in enumerate(string))


class UUIDEncoder(JSONEncoder):
    """JSON Encoder for UUIDs."""

    def default(self, obj: Any) -> Any:
        """Handle UUIDs.

        Args:
            obj: The object to encode

        Returns:
            str: The encoded object
        """
        return str(obj) if isinstance(obj, UUID) else super().default(obj)
