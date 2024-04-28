"""Calculator Controller."""

from __future__ import annotations

from typing import Annotated

from litestar import Controller, get
from litestar.contrib.htmx.request import HTMXRequest  # noqa: TCH002
from litestar.contrib.htmx.response import HTMXTemplate
from litestar.params import Parameter  # noqa: TCH002
from litestar.status_codes import HTTP_200_OK

from app.domain import urls
from app.domain.calculator.helpers import get_network_info
from app.domain.calculator.schema import NetworkInfo

__all__ = ("CalculatorController",)


class CalculatorController(Controller):
    """Calculator Controller."""

    opt = {"exclude_from_auth": True}

    @get(
        path=f"{urls.IP}",
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
    ) -> NetworkInfo:
        """Calculate IP.

        Args:
            request: HTMXRequest
            ip: The IP address in standard IPv4 format.
            prefix: The CIDR notation.

        Returns:
            The network information rendered via the schema object.
        """
        network_info = get_network_info(ip, prefix)

        return NetworkInfo(
            subnet_mask=network_info.subnet_mask,
            wildcard_subnet_mask=network_info.wildcard_subnet_mask,
            total_ips=network_info.total_ips,
            usable_ips=network_info.usable_ips,
            network_ip=network_info.network_ip,
            broadcast_ip=network_info.broadcast_ip,
            first_ip=network_info.first_ip,
            last_ip=network_info.last_ip,
        )

    @get(
        path=f"{urls.IP}/htmx",
        operation_id="CalculatorIPHTMX",
        name="calculator:ip:htmx",
        status_code=HTTP_200_OK,
    )
    async def ip_htmx(
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
        network_info = get_network_info(ip, prefix)

        return HTMXTemplate(
            template_name="partial.html",
            context={"network_info": network_info.model_dump(by_alias=True)},
            push_url=False,
        )
