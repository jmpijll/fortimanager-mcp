"""MCP tools for VPN management."""

import logging
from typing import Any

from fortimanager_mcp.api.vpn import VPNAPI
from fortimanager_mcp.server import get_fmg_client, mcp

logger = logging.getLogger(__name__)


def _get_vpn_api() -> VPNAPI:
    """Get VPN API instance with FortiManager client."""
    client = get_fmg_client()
    if client is None:
        raise RuntimeError("FortiManager client not initialized")
    return VPNAPI(client)


# =============================================================================
# IPsec Phase1 Tools
# =============================================================================


@mcp.tool()
async def list_ipsec_phase1_interfaces(adom: str = "root") -> dict[str, Any]:
    """List all IPsec Phase1 interfaces in an ADOM.
    
    IPsec Phase1 defines the main VPN tunnel parameters including:
    - Authentication method (PSK or certificate)
    - IKE version and encryption settings
    - Remote gateway configuration
    - DPD (Dead Peer Detection) settings
    
    Args:
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with status and list of Phase1 interfaces
    """
    api = _get_vpn_api()
    interfaces = await api.list_ipsec_phase1(adom=adom)
    return {
        "status": "success",
        "count": len(interfaces),
        "interfaces": interfaces,
    }


@mcp.tool()
async def get_ipsec_phase1_interface(
    name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Get detailed information about a specific IPsec Phase1 interface.
    
    Args:
        name: Phase1 interface name
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with status and Phase1 interface details
    """
    api = _get_vpn_api()
    interface = await api.get_ipsec_phase1(name=name, adom=adom)
    return {
        "status": "success",
        "interface": interface,
    }


@mcp.tool()
async def create_ipsec_phase1_interface(
    name: str,
    interface: str,
    remote_gw: str,
    adom: str = "root",
    psk: str | None = None,
    certificate: str | None = None,
    ike_version: int = 2,
    proposal: str = "aes128-sha256",
) -> dict[str, Any]:
    """Create a new IPsec Phase1 interface.
    
    This creates the main VPN tunnel configuration. You must specify either
    PSK (pre-shared key) or certificate for authentication.
    
    Args:
        name: Phase1 interface name
        interface: Physical/logical interface name (e.g., "port1", "wan1")
        remote_gw: Remote gateway IP address
        adom: ADOM name (default: root)
        psk: Pre-shared key (for PSK authentication)
        certificate: Certificate name (for certificate authentication)
        ike_version: IKE version (1 or 2, default: 2)
        proposal: Encryption proposal (default: aes128-sha256)
    
    Returns:
        Dictionary with status and created interface details
    """
    api = _get_vpn_api()
    result = await api.create_ipsec_phase1(
        name=name,
        interface=interface,
        remote_gw=remote_gw,
        adom=adom,
        psk=psk,
        certificate=certificate,
        ike_version=ike_version,
        proposal=proposal,
    )
    return {
        "status": "success",
        "interface": result,
    }


@mcp.tool()
async def delete_ipsec_phase1_interface(
    name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Delete an IPsec Phase1 interface.
    
    WARNING: This will delete the main VPN tunnel configuration. All associated
    Phase2 interfaces should be deleted first.
    
    Args:
        name: Phase1 interface name
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with deletion status
    """
    api = _get_vpn_api()
    result = await api.delete_ipsec_phase1(name=name, adom=adom)
    return {
        "status": "success",
        "result": result,
    }


# =============================================================================
# IPsec Phase2 Tools
# =============================================================================


@mcp.tool()
async def list_ipsec_phase2_interfaces(adom: str = "root") -> dict[str, Any]:
    """List all IPsec Phase2 interfaces in an ADOM.
    
    IPsec Phase2 defines the traffic selectors (source/destination subnets)
    and encryption settings for data traffic through the VPN tunnel.
    
    Args:
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with status and list of Phase2 interfaces
    """
    api = _get_vpn_api()
    interfaces = await api.list_ipsec_phase2(adom=adom)
    return {
        "status": "success",
        "count": len(interfaces),
        "interfaces": interfaces,
    }


@mcp.tool()
async def get_ipsec_phase2_interface(
    name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Get detailed information about a specific IPsec Phase2 interface.
    
    Args:
        name: Phase2 interface name
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with status and Phase2 interface details
    """
    api = _get_vpn_api()
    interface = await api.get_ipsec_phase2(name=name, adom=adom)
    return {
        "status": "success",
        "interface": interface,
    }


@mcp.tool()
async def create_ipsec_phase2_interface(
    name: str,
    phase1name: str,
    adom: str = "root",
    src_subnet: str | None = None,
    dst_subnet: str | None = None,
) -> dict[str, Any]:
    """Create a new IPsec Phase2 interface.
    
    Phase2 defines which traffic is allowed through the VPN tunnel by
    specifying source and destination subnets.
    
    Args:
        name: Phase2 interface name
        phase1name: Associated Phase1 interface name
        adom: ADOM name (default: root)
        src_subnet: Source subnet in CIDR format (e.g., "192.168.1.0/24")
        dst_subnet: Destination subnet in CIDR format
    
    Returns:
        Dictionary with status and created interface details
    """
    api = _get_vpn_api()
    result = await api.create_ipsec_phase2(
        name=name,
        phase1name=phase1name,
        adom=adom,
        src_subnet=src_subnet,
        dst_subnet=dst_subnet,
    )
    return {
        "status": "success",
        "interface": result,
    }


@mcp.tool()
async def delete_ipsec_phase2_interface(
    name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Delete an IPsec Phase2 interface.
    
    Args:
        name: Phase2 interface name
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with deletion status
    """
    api = _get_vpn_api()
    result = await api.delete_ipsec_phase2(name=name, adom=adom)
    return {
        "status": "success",
        "result": result,
    }


# =============================================================================
# SSL-VPN Portal Tools
# =============================================================================


@mcp.tool()
async def list_sslvpn_portals(adom: str = "root") -> dict[str, Any]:
    """List all SSL-VPN portals in an ADOM.
    
    SSL-VPN portals define the user experience and access rights for
    SSL-VPN connections. Each portal can have different settings for:
    - Tunnel mode (full VPN client)
    - Web mode (clientless browser access)
    - Split tunneling configuration
    - Bookmarks and access restrictions
    
    Args:
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with status and list of portals
    """
    api = _get_vpn_api()
    portals = await api.list_sslvpn_portals(adom=adom)
    return {
        "status": "success",
        "count": len(portals),
        "portals": portals,
    }


@mcp.tool()
async def get_sslvpn_portal(
    name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Get detailed information about a specific SSL-VPN portal.
    
    Args:
        name: Portal name
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with status and portal details
    """
    api = _get_vpn_api()
    portal = await api.get_sslvpn_portal(name=name, adom=adom)
    return {
        "status": "success",
        "portal": portal,
    }


@mcp.tool()
async def create_sslvpn_portal(
    name: str,
    adom: str = "root",
    tunnel_mode: bool = True,
    web_mode: bool = True,
) -> dict[str, Any]:
    """Create a new SSL-VPN portal.
    
    Args:
        name: Portal name
        adom: ADOM name (default: root)
        tunnel_mode: Enable tunnel mode (full VPN client)
        web_mode: Enable web mode (clientless browser access)
    
    Returns:
        Dictionary with status and created portal details
    """
    api = _get_vpn_api()
    result = await api.create_sslvpn_portal(
        name=name,
        adom=adom,
        tunnel_mode=tunnel_mode,
        web_mode=web_mode,
    )
    return {
        "status": "success",
        "portal": result,
    }


@mcp.tool()
async def delete_sslvpn_portal(
    name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Delete an SSL-VPN portal.
    
    WARNING: Ensure the portal is not assigned to any user groups before deletion.
    
    Args:
        name: Portal name
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with deletion status
    """
    api = _get_vpn_api()
    result = await api.delete_sslvpn_portal(name=name, adom=adom)
    return {
        "status": "success",
        "result": result,
    }


# =============================================================================
# VPN Certificate Tools
# =============================================================================


@mcp.tool()
async def list_vpn_ca_certificates(adom: str = "root") -> dict[str, Any]:
    """List all VPN Certificate Authorities in an ADOM.
    
    CA certificates are used to validate remote peer certificates in
    certificate-based VPN authentication.
    
    Args:
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with status and list of CA certificates
    """
    api = _get_vpn_api()
    certificates = await api.list_vpn_certificates_ca(adom=adom)
    return {
        "status": "success",
        "count": len(certificates),
        "certificates": certificates,
    }


@mcp.tool()
async def get_vpn_ca_certificate(
    name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Get detailed information about a specific VPN CA certificate.
    
    Args:
        name: CA certificate name
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with status and CA certificate details
    """
    api = _get_vpn_api()
    certificate = await api.get_vpn_certificate_ca(name=name, adom=adom)
    return {
        "status": "success",
        "certificate": certificate,
    }


@mcp.tool()
async def list_vpn_remote_certificates(adom: str = "root") -> dict[str, Any]:
    """List all VPN remote certificates in an ADOM.
    
    Remote certificates are peer certificates imported for validation
    in certificate-based VPN authentication.
    
    Args:
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with status and list of remote certificates
    """
    api = _get_vpn_api()
    certificates = await api.list_vpn_certificates_remote(adom=adom)
    return {
        "status": "success",
        "count": len(certificates),
        "certificates": certificates,
    }


@mcp.tool()
async def get_vpn_remote_certificate(
    name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Get detailed information about a specific VPN remote certificate.
    
    Args:
        name: Remote certificate name
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with status and remote certificate details
    """
    api = _get_vpn_api()
    certificate = await api.get_vpn_certificate_remote(name=name, adom=adom)
    return {
        "status": "success",
        "certificate": certificate,
    }


# =============================================================================
# SSL-VPN Host Check Tools
# =============================================================================


@mcp.tool()
async def list_sslvpn_host_check_software(adom: str = "root") -> dict[str, Any]:
    """List all SSL-VPN host check software configurations in an ADOM.
    
    Host check software configurations define endpoint compliance checks
    that SSL-VPN clients must pass before establishing a connection. This
    includes checking for:
    - Antivirus software
    - Firewall status
    - Operating system patches
    - Registry keys
    - Running processes
    
    Args:
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with status and list of host check software
    """
    api = _get_vpn_api()
    software = await api.list_sslvpn_host_check_software(adom=adom)
    return {
        "status": "success",
        "count": len(software),
        "software": software,
    }


@mcp.tool()
async def get_sslvpn_host_check_software(
    name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Get detailed information about a specific SSL-VPN host check software configuration.
    
    Args:
        name: Host check software name
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with status and host check software details
    """
    api = _get_vpn_api()
    software = await api.get_sslvpn_host_check_software(name=name, adom=adom)
    return {
        "status": "success",
        "software": software,
    }


# ============================================================================
# Phase 23: Advanced VPN/IPsec - IPsec Advanced Operations
# ============================================================================


@mcp.tool()
async def list_ipsec_concentrators(adom: str = "root") -> dict[str, Any]:
    """List IPsec VPN concentrator configurations.
    
    Concentrators allow a single FortiGate to act as an aggregation point
    for multiple IPsec tunnels from remote sites, providing centralized
    VPN connectivity.
    
    Use cases:
    - Hub-and-spoke VPN topologies
    - Central office connectivity
    - Aggregating branch office VPNs
    
    Args:
        adom: ADOM name (default: "root")
    
    Returns:
        Dictionary with list of concentrator configs
    
    Example:
        result = list_ipsec_concentrators(adom="root")
    """
    api = _get_vpn_api()
    concentrators = await api.list_ipsec_concentrators(adom=adom)
    return {
        "status": "success",
        "count": len(concentrators),
        "concentrators": concentrators,
    }


@mcp.tool()
async def list_ipsec_forticlient_templates(adom: str = "root") -> dict[str, Any]:
    """List FortiClient IPsec VPN templates.
    
    Templates define standardized FortiClient VPN connection settings
    that can be distributed to end users for consistent and easy
    VPN configuration across the organization.
    
    Templates include:
    - Authentication settings
    - Connection parameters
    - Security settings
    - Auto-connect rules
    
    Args:
        adom: ADOM name (default: "root")
    
    Returns:
        Dictionary with list of FortiClient templates
    
    Example:
        result = list_ipsec_forticlient_templates(adom="root")
    """
    api = _get_vpn_api()
    templates = await api.list_ipsec_forticlient_templates(adom=adom)
    return {
        "status": "success",
        "count": len(templates),
        "templates": templates,
    }


@mcp.tool()
async def list_ipsec_manualkey_interfaces(adom: str = "root") -> dict[str, Any]:
    """List IPsec manual-key interfaces.
    
    Manual-key IPsec interfaces use pre-configured cryptographic keys
    instead of IKE (Internet Key Exchange) for tunnel establishment.
    This is less common but used in specific scenarios requiring
    static key management.
    
    Manual-key is typically used for:
    - Legacy system compatibility
    - Specific security requirements
    - Simplified configuration in controlled environments
    
    Args:
        adom: ADOM name (default: "root")
    
    Returns:
        Dictionary with list of manual-key interfaces
    
    Example:
        result = list_ipsec_manualkey_interfaces(adom="root")
    """
    api = _get_vpn_api()
    interfaces = await api.list_ipsec_manualkey_interfaces(adom=adom)
    return {
        "status": "success",
        "count": len(interfaces),
        "interfaces": interfaces,
    }


# ============================================================================
# Phase 23: Advanced VPN/IPsec - VPN Monitoring
# ============================================================================


@mcp.tool()
async def get_ipsec_tunnel_status(
    device: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Get IPsec tunnel status for a device.
    
    Retrieves real-time status of all IPsec VPN tunnels on a specific
    FortiGate device, including:
    - Tunnel up/down status
    - Phase 1 and Phase 2 connection state
    - Remote peer information
    - Traffic statistics (bytes/packets)
    - Connection uptime
    - Last negotiation time
    
    Use this to:
    - Monitor VPN connectivity
    - Troubleshoot tunnel issues
    - Verify tunnel establishment
    - Track VPN usage
    
    Args:
        device: Device name
        adom: ADOM name (default: "root")
    
    Returns:
        Dictionary with list of tunnel status entries
    
    Example:
        result = get_ipsec_tunnel_status(
            device="FGT-HQ-01",
            adom="root"
        )
    """
    api = _get_vpn_api()
    status = await api.get_ipsec_tunnel_status(device=device, adom=adom)
    return {
        "status": "success",
        "device": device,
        "tunnel_count": len(status),
        "tunnels": status,
    }


@mcp.tool()
async def get_sslvpn_tunnel_status(
    device: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Get SSL-VPN tunnel status for a device.
    
    Retrieves information about active SSL-VPN connections on a FortiGate:
    - Currently connected users
    - Connection duration
    - Data transferred (upload/download)
    - Client IP addresses
    - Authentication method used
    - Virtual IP assigned
    - Tunnel routes
    
    Use this to:
    - Monitor remote user connectivity
    - Track SSL-VPN usage
    - Identify active users
    - Troubleshoot connection issues
    
    Args:
        device: Device name
        adom: ADOM name (default: "root")
    
    Returns:
        Dictionary with list of active SSL-VPN sessions
    
    Example:
        result = get_sslvpn_tunnel_status(
            device="FGT-HQ-01",
            adom="root"
        )
    """
    api = _get_vpn_api()
    status = await api.get_sslvpn_tunnel_status(device=device, adom=adom)
    return {
        "status": "success",
        "device": device,
        "active_sessions": len(status),
        "sessions": status,
    }


@mcp.tool()
async def get_vpn_statistics(
    device: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Get VPN statistics for a device.
    
    Retrieves comprehensive VPN statistics and metrics:
    - Total configured tunnels (IPsec + SSL-VPN)
    - Currently active tunnels
    - Total data throughput
    - Packet counts and statistics
    - Error counters
    - Encryption/decryption stats
    
    Use this for:
    - Capacity planning
    - Performance monitoring
    - Usage reporting
    - Troubleshooting VPN performance
    
    Args:
        device: Device name
        adom: ADOM name (default: "root")
    
    Returns:
        Dictionary with VPN statistics
    
    Example:
        result = get_vpn_statistics(
            device="FGT-HQ-01",
            adom="root"
        )
    """
    api = _get_vpn_api()
    stats = await api.get_vpn_statistics(device=device, adom=adom)
    return {
        "status": "success",
        "device": device,
        "statistics": stats,
    }

