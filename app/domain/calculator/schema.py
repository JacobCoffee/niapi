"""NIAPI calculator schema."""
from __future__ import annotations

from typing import Annotated

from pydantic import BaseModel, Field

__all__ = ("NetworkData",)


class NetworkData(BaseModel):
    """Network Data Schema."""

    ip: Annotated[
        int,
        Field(
            ...,
            description="The IP address in standard IPv4 format.",
            regex=r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$",
        ),
    ]

    cidr: Annotated[
        int,
        Field(
            ...,
            description="The CIDR notation.",
            regex=r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\/([0-9]|[1-2][0-9]|3[0-2])$",
        ),
    ]
