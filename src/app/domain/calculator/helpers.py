"""Helpers for calculator domain module."""

import ipaddress

from app.domain.calculator.schema import NetworkInfo

__all__ = ("get_network_info",)


def get_network_info(ip: str, prefix: str) -> NetworkInfo:
    """Get network information.

    Args:
        ip: The IP address in standard IPv4 format.
        prefix: The CIDR notation.

    Returns:
        NetworkInfo: The network information.
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

    return NetworkInfo(
        subnet_mask=subnet_mask,
        wildcard_subnet_mask=wildcard_subnet_mask,
        total_ips=total_ips,
        usable_ips=usable_ips,
        network_ip=network_ip,
        broadcast_ip=broadcast_ip,
        first_ip=first_ip,
        last_ip=last_ip,
    )
