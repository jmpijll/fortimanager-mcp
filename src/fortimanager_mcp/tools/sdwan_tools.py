"""MCP tools for SD-WAN management."""

from typing import Any

from fortimanager_mcp.api.sdwan import SdwanAPI
from fortimanager_mcp.server import get_fmg_client, mcp


def _get_sdwan_api() -> SdwanAPI:
    """Get SD-WAN API instance."""
    client = get_fmg_client()
    return SdwanAPI(client)


# ============================================================================
# SD-WAN Zones
# ============================================================================

@mcp.tool()
async def list_sdwan_zones(adom: str = "root") -> dict[str, Any]:
    """List SD-WAN zones in an ADOM.
    
    SD-WAN zones group WAN interfaces for load balancing and failover.
    
    Args:
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with status and list of SD-WAN zones
    """
    api = _get_sdwan_api()
    zones = await api.list_sdwan_zones(adom=adom)
    return {"status": "success", "count": len(zones), "zones": zones}


@mcp.tool()
async def get_sdwan_zone(name: str, adom: str = "root") -> dict[str, Any]:
    """Get SD-WAN zone details.
    
    Args:
        name: Zone name
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with zone details
    """
    api = _get_sdwan_api()
    zone = await api.get_sdwan_zone(name=name, adom=adom)
    return {"status": "success", "zone": zone}


@mcp.tool()
async def create_sdwan_zone(
    name: str,
    adom: str = "root",
    service_sla_tie_break: str = "zone",
) -> dict[str, Any]:
    """Create an SD-WAN zone.
    
    Args:
        name: Zone name
        adom: ADOM name (default: root)
        service_sla_tie_break: SLA tie-break method (default: zone)
    
    Returns:
        Dictionary with creation result
    """
    api = _get_sdwan_api()
    result = await api.create_sdwan_zone(
        name=name,
        adom=adom,
        service_sla_tie_break=service_sla_tie_break,
    )
    return {"status": "success", "result": result}


@mcp.tool()
async def delete_sdwan_zone(name: str, adom: str = "root") -> dict[str, Any]:
    """Delete an SD-WAN zone.
    
    Args:
        name: Zone name
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with deletion result
    """
    api = _get_sdwan_api()
    result = await api.delete_sdwan_zone(name=name, adom=adom)
    return {"status": "success", "result": result}


# ============================================================================
# SD-WAN Health Checks
# ============================================================================

@mcp.tool()
async def list_sdwan_health_checks(adom: str = "root") -> dict[str, Any]:
    """List SD-WAN health check monitors.
    
    Health checks monitor link quality and availability for SD-WAN members.
    
    Args:
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with status and list of health checks
    """
    api = _get_sdwan_api()
    health_checks = await api.list_sdwan_health_checks(adom=adom)
    return {"status": "success", "count": len(health_checks), "health_checks": health_checks}


@mcp.tool()
async def get_sdwan_health_check(name: str, adom: str = "root") -> dict[str, Any]:
    """Get SD-WAN health check details.
    
    Args:
        name: Health check name
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with health check details
    """
    api = _get_sdwan_api()
    health_check = await api.get_sdwan_health_check(name=name, adom=adom)
    return {"status": "success", "health_check": health_check}


@mcp.tool()
async def create_sdwan_health_check(
    name: str,
    server: str,
    protocol: str = "ping",
    interval: int = 1000,
    probe_timeout: int = 500,
    adom: str = "root",
) -> dict[str, Any]:
    """Create an SD-WAN health check monitor.
    
    Args:
        name: Health check name
        server: Server IP address to monitor
        protocol: Protocol to use (ping, tcp-echo, udp-echo, http, dns, etc.)
        interval: Probe interval in milliseconds (default: 1000)
        probe_timeout: Probe timeout in milliseconds (default: 500)
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with creation result
    """
    api = _get_sdwan_api()
    result = await api.create_sdwan_health_check(
        name=name,
        server=server,
        protocol=protocol,
        interval=interval,
        probe_timeout=probe_timeout,
        adom=adom,
    )
    return {"status": "success", "result": result}


@mcp.tool()
async def delete_sdwan_health_check(name: str, adom: str = "root") -> dict[str, Any]:
    """Delete an SD-WAN health check.
    
    Args:
        name: Health check name
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with deletion result
    """
    api = _get_sdwan_api()
    result = await api.delete_sdwan_health_check(name=name, adom=adom)
    return {"status": "success", "result": result}


# ============================================================================
# SD-WAN Services (Rules)
# ============================================================================

@mcp.tool()
async def list_sdwan_services(adom: str = "root") -> dict[str, Any]:
    """List SD-WAN service rules.
    
    Service rules determine which path traffic should take based on various criteria
    (application, destination, SLA requirements, etc.).
    
    Args:
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with status and list of service rules
    """
    api = _get_sdwan_api()
    services = await api.list_sdwan_services(adom=adom)
    return {"status": "success", "count": len(services), "services": services}


@mcp.tool()
async def get_sdwan_service(service_id: int, adom: str = "root") -> dict[str, Any]:
    """Get SD-WAN service rule details.
    
    Args:
        service_id: Service rule ID
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with service rule details
    """
    api = _get_sdwan_api()
    service = await api.get_sdwan_service(service_id=service_id, adom=adom)
    return {"status": "success", "service": service}


@mcp.tool()
async def create_sdwan_service(
    name: str,
    mode: str = "manual",
    dst: list[str] | None = None,
    src: list[str] | None = None,
    priority_members: list[str] | None = None,
    adom: str = "root",
) -> dict[str, Any]:
    """Create an SD-WAN service rule.
    
    Args:
        name: Service rule name
        mode: Service mode (auto, manual, priority, sla)
        dst: Destination address/subnet list
        src: Source address/subnet list
        priority_members: Priority member interfaces (for manual/priority mode)
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with creation result
    """
    api = _get_sdwan_api()
    kwargs = {}
    if dst:
        kwargs["dst"] = dst
    if src:
        kwargs["src"] = src
    if priority_members:
        kwargs["priority-members"] = priority_members
    
    result = await api.create_sdwan_service(
        name=name,
        mode=mode,
        adom=adom,
        **kwargs,
    )
    return {"status": "success", "result": result}


@mcp.tool()
async def delete_sdwan_service(service_id: int, adom: str = "root") -> dict[str, Any]:
    """Delete an SD-WAN service rule.
    
    Args:
        service_id: Service rule ID
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with deletion result
    """
    api = _get_sdwan_api()
    result = await api.delete_sdwan_service(service_id=service_id, adom=adom)
    return {"status": "success", "result": result}


# ============================================================================
# SD-WAN Members
# ============================================================================

@mcp.tool()
async def list_sdwan_members(adom: str = "root") -> dict[str, Any]:
    """List SD-WAN member interfaces.
    
    Members are the WAN interfaces participating in SD-WAN for load balancing
    and failover.
    
    Args:
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with status and list of member interfaces
    """
    api = _get_sdwan_api()
    members = await api.list_sdwan_members(adom=adom)
    return {"status": "success", "count": len(members), "members": members}


# ============================================================================
# Traffic Classes
# ============================================================================

@mcp.tool()
async def list_traffic_classes(adom: str = "root") -> dict[str, Any]:
    """List traffic classes for SD-WAN application-based routing.
    
    Traffic classes define application categories for intelligent routing decisions.
    
    Args:
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with status and list of traffic classes
    """
    api = _get_sdwan_api()
    classes = await api.list_traffic_classes(adom=adom)
    return {"status": "success", "count": len(classes), "classes": classes}


@mcp.tool()
async def get_traffic_class(class_id: int, adom: str = "root") -> dict[str, Any]:
    """Get traffic class details.
    
    Args:
        class_id: Traffic class ID
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with traffic class details
    """
    api = _get_sdwan_api()
    traffic_class = await api.get_traffic_class(class_id=class_id, adom=adom)
    return {"status": "success", "class": traffic_class}


@mcp.tool()
async def create_traffic_class(
    class_name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Create a traffic class.
    
    Args:
        class_name: Traffic class name
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with creation result
    """
    api = _get_sdwan_api()
    result = await api.create_traffic_class(class_name=class_name, adom=adom)
    return {"status": "success", "result": result}


@mcp.tool()
async def delete_traffic_class(class_id: int, adom: str = "root") -> dict[str, Any]:
    """Delete a traffic class.
    
    Args:
        class_id: Traffic class ID
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with deletion result
    """
    api = _get_sdwan_api()
    result = await api.delete_traffic_class(class_id=class_id, adom=adom)
    return {"status": "success", "result": result}


# ============================================================================
# WAN Profiles
# ============================================================================

@mcp.tool()
async def list_wan_profiles(adom: str = "root") -> dict[str, Any]:
    """List WAN profiles (SD-WAN templates).
    
    WAN profiles are templates for SD-WAN configuration that can be applied
    to multiple devices.
    
    Args:
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with status and list of WAN profiles
    """
    api = _get_sdwan_api()
    profiles = await api.list_wan_profiles(adom=adom)
    return {"status": "success", "count": len(profiles), "profiles": profiles}


@mcp.tool()
async def get_wan_profile(name: str, adom: str = "root") -> dict[str, Any]:
    """Get WAN profile details.
    
    Args:
        name: WAN profile name
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with WAN profile details
    """
    api = _get_sdwan_api()
    profile = await api.get_wan_profile(name=name, adom=adom)
    return {"status": "success", "profile": profile}

