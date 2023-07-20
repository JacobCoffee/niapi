"""NIAPI calculator schema."""
from __future__ import annotations

from typing import Annotated

from pydantic import BaseModel, Field

__all__ = ("NetworkData", "NetworkInfo")


class NetworkData(BaseModel):
    """Network Data Schema."""

    ip: Annotated[
        str,
        Field(
            ...,
            description="The IP address in standard IPv4 format.",
            regex=r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$",
        ),
    ]

    prefix: Annotated[
        str,
        Field(
            ...,
            description="The Subnet Prefix.",
            regex=r"^(3[012]|[12]?\d)$",
        ),
    ]


class NetworkInfo(BaseModel):
    """Network Info Schema."""

    subnet_mask: Annotated[
        str,
        Field(
            ...,
            description="The subnet mask in standard IPv4 format.",
            regex=r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$",
        ),
    ]
    wildcard_subnet_mask: Annotated[
        str,
        Field(
            ...,
            description="The wildcard subnet mask in standard IPv4 format.",
            regex=r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$",
        ),
    ]
    total_ips: Annotated[int, Field(..., description="The total number of IPs in the network.")]
    usable_ips: Annotated[int, Field(..., description="The total number of usable IPs in the network.")]
    network_ip: Annotated[
        str, Field(..., description="The network IP in standard IPv4 format.", regex=r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
    ]
    broadcast_ip: Annotated[
        str,
        Field(..., description="The broadcast IP in standard IPv4 format.", regex=r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"),
    ]
    first_ip: Annotated[
        str, Field(..., description="The first IP in standard IPv4 format.", regex=r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
    ]
    last_ip: Annotated[
        str, Field(..., description="The last IP in standard IPv4 format.", regex=r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
    ]
