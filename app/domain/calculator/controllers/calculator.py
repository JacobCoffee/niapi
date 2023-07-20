"""Calculator Controller."""
from __future__ import annotations

import ipaddress
from typing import Annotated

from litestar import Controller, get

__all__ = ["CalculatorController"]

from litestar.params import Parameter  # noqa
from litestar.status_codes import HTTP_200_OK
from litestar.contrib.htmx.response import HTMXTemplate

from app.domain import urls
from app.domain.calculator.schema import NetworkInfo

from litestar.contrib.htmx.request import HTMXRequest  # noqa


class CalculatorController(Controller):
    """Calculator Controller."""

    opt = {"exclude_from_auth": True}

    @get(
        path=urls.IP,
        operation_id="CalculatorIP",
        name="calculator:ip",
        status_code=HTTP_200_OK,
    )
    async def ip(
        self,
        request: HTMXRequest,
        ip: Annotated[
            str,
            Parameter(
                ...,
                description="The IP address in standard IPv4 format.",
                pattern=r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$",
            ),
        ],
        prefix: Annotated[
            str, Parameter(..., description="The CIDR notation.", pattern=r"^(?:[0-9]|[1-2][0-9]|3[0-2])$")
        ],
    ) -> HTMXTemplate:
        """Calculate IP.

        Args:
            request: HTMXRequest
            ip: The IP address in standard IPv4 format.
            prefix: The CIDR notation.

        Returns:
            The request data via HTMX as a template passed to partial.html
        """

        net = ipaddress.IPv4Network(f"{ip}/{prefix}", strict=False)

        subnet_mask = str(net.netmask)
        wildcard_subnet_mask = str(net.hostmask)
        total_ips = net.num_addresses
        usable_ips = total_ips - 2  # minus network and broadcast addresses
        network_ip = str(net.network_address)
        broadcast_ip = str(net.broadcast_address)

        # First and last usable IP addresses
        hosts = list(net.hosts())
        first_ip = str(hosts[0]) if hosts else None
        last_ip = str(hosts[-1]) if hosts else None

        network_info = NetworkInfo(
            subnet_mask=subnet_mask,
            wildcard_subnet_mask=wildcard_subnet_mask,
            total_ips=total_ips,
            usable_ips=usable_ips,
            network_ip=network_ip,
            broadcast_ip=broadcast_ip,
            first_ip=first_ip,
            last_ip=last_ip,
        )

        return HTMXTemplate(
            template_name="partial.html",
            context=network_info.dict(),  # Convert the pydantic model to a dict
            push_url=False,
        )
