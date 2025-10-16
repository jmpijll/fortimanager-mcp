"""MCP tools for advanced firewall objects."""

import logging
from typing import Any

from fortimanager_mcp.api.advanced_objects import AdvancedObjectsAPI
from fortimanager_mcp.server import get_fmg_client, mcp

logger = logging.getLogger(__name__)


def _get_advanced_objects_api() -> AdvancedObjectsAPI:
    """Get Advanced Objects API instance."""
    client = get_fmg_client()
    return AdvancedObjectsAPI(client)


# ============================================================================
# Virtual IPs (VIPs)
# ============================================================================

@mcp.tool()
async def list_virtual_ips(adom: str = "root") -> dict[str, Any]:
    """List all virtual IPs (VIPs) in an ADOM.
    
    VIPs are used for destination NAT and port forwarding to internal servers.
    
    Args:
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with VIPs list
        
    Example:
        # List all VIPs for port forwarding rules
        result = list_virtual_ips(adom="production")
    """
    try:
        api = _get_advanced_objects_api()
        vips = await api.list_vips(adom=adom)
        return {
            "status": "success",
            "count": len(vips),
            "vips": vips,
        }
    except Exception as e:
        logger.error(f"Error listing VIPs in ADOM {adom}: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_virtual_ip(name: str, adom: str = "root") -> dict[str, Any]:
    """Get details of a specific virtual IP.
    
    Args:
        name: VIP name
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with VIP details
    """
    try:
        api = _get_advanced_objects_api()
        vip = await api.get_vip(name=name, adom=adom)
        return {
            "status": "success",
            "vip": vip,
        }
    except Exception as e:
        logger.error(f"Error getting VIP '{name}': {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def create_virtual_ip(
    name: str,
    extip: str,
    mappedip: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Create a virtual IP for destination NAT or port forwarding.
    
    Args:
        name: VIP name
        extip: External IP address or range
        mappedip: Internal (mapped) IP address or range
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with creation result
        
    Example:
        # Create VIP for web server
        result = create_virtual_ip(
            name="web-server-vip",
            extip="203.0.113.10",
            mappedip="192.168.1.10",
            adom="production"
        )
    """
    try:
        api = _get_advanced_objects_api()
        result = await api.create_vip(
            name=name,
            extip=extip,
            mappedip=mappedip,
            adom=adom,
        )
        return {
            "status": "success",
            "message": f"VIP '{name}' created successfully",
            "result": result,
        }
    except Exception as e:
        logger.error(f"Error creating VIP '{name}': {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def delete_virtual_ip(name: str, adom: str = "root") -> dict[str, Any]:
    """Delete a virtual IP.
    
    Args:
        name: VIP name
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with deletion result
    """
    try:
        api = _get_advanced_objects_api()
        result = await api.delete_vip(name=name, adom=adom)
        return {
            "status": "success",
            "message": f"VIP '{name}' deleted successfully",
            "result": result,
        }
    except Exception as e:
        logger.error(f"Error deleting VIP '{name}': {e}")
        return {"status": "error", "message": str(e)}


# ============================================================================
# VIP Groups
# ============================================================================

@mcp.tool()
async def list_vip_groups(adom: str = "root") -> dict[str, Any]:
    """List all VIP groups in an ADOM.
    
    Args:
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with VIP groups list
    """
    try:
        api = _get_advanced_objects_api()
        groups = await api.list_vip_groups(adom=adom)
        return {
            "status": "success",
            "count": len(groups),
            "vip_groups": groups,
        }
    except Exception as e:
        logger.error(f"Error listing VIP groups in ADOM {adom}: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def create_vip_group(
    name: str,
    members: list[str],
    adom: str = "root",
) -> dict[str, Any]:
    """Create a VIP group.
    
    Args:
        name: VIP group name
        members: List of VIP names to include in the group
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with creation result
        
    Example:
        result = create_vip_group(
            name="dmz-servers",
            members=["web-vip", "mail-vip", "ftp-vip"],
            adom="production"
        )
    """
    try:
        api = _get_advanced_objects_api()
        result = await api.create_vip_group(
            name=name,
            members=members,
            adom=adom,
        )
        return {
            "status": "success",
            "message": f"VIP group '{name}' created with {len(members)} members",
            "result": result,
        }
    except Exception as e:
        logger.error(f"Error creating VIP group '{name}': {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def delete_vip_group(name: str, adom: str = "root") -> dict[str, Any]:
    """Delete a VIP group.
    
    Args:
        name: VIP group name
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with deletion result
    """
    try:
        api = _get_advanced_objects_api()
        result = await api.delete_vip_group(name=name, adom=adom)
        return {
            "status": "success",
            "message": f"VIP group '{name}' deleted successfully",
            "result": result,
        }
    except Exception as e:
        logger.error(f"Error deleting VIP group '{name}': {e}")
        return {"status": "error", "message": str(e)}


# ============================================================================
# IP Pools
# ============================================================================

@mcp.tool()
async def list_ip_pools(adom: str = "root") -> dict[str, Any]:
    """List all IP pools in an ADOM.
    
    IP pools are used for source NAT (SNAT) when accessing the internet.
    
    Args:
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with IP pools list
    """
    try:
        api = _get_advanced_objects_api()
        pools = await api.list_ip_pools(adom=adom)
        return {
            "status": "success",
            "count": len(pools),
            "ip_pools": pools,
        }
    except Exception as e:
        logger.error(f"Error listing IP pools in ADOM {adom}: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_ip_pool(name: str, adom: str = "root") -> dict[str, Any]:
    """Get details of a specific IP pool.
    
    Args:
        name: IP pool name
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with IP pool details
    """
    try:
        api = _get_advanced_objects_api()
        pool = await api.get_ip_pool(name=name, adom=adom)
        return {
            "status": "success",
            "ip_pool": pool,
        }
    except Exception as e:
        logger.error(f"Error getting IP pool '{name}': {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def create_ip_pool(
    name: str,
    startip: str,
    endip: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Create an IP pool for source NAT.
    
    Args:
        name: IP pool name
        startip: Starting IP address
        endip: Ending IP address
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with creation result
        
    Example:
        # Create IP pool for internet access
        result = create_ip_pool(
            name="internet-nat-pool",
            startip="203.0.113.100",
            endip="203.0.113.199",
            adom="production"
        )
    """
    try:
        api = _get_advanced_objects_api()
        result = await api.create_ip_pool(
            name=name,
            startip=startip,
            endip=endip,
            adom=adom,
        )
        return {
            "status": "success",
            "message": f"IP pool '{name}' created ({startip} - {endip})",
            "result": result,
        }
    except Exception as e:
        logger.error(f"Error creating IP pool '{name}': {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def delete_ip_pool(name: str, adom: str = "root") -> dict[str, Any]:
    """Delete an IP pool.
    
    Args:
        name: IP pool name
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with deletion result
    """
    try:
        api = _get_advanced_objects_api()
        result = await api.delete_ip_pool(name=name, adom=adom)
        return {
            "status": "success",
            "message": f"IP pool '{name}' deleted successfully",
            "result": result,
        }
    except Exception as e:
        logger.error(f"Error deleting IP pool '{name}': {e}")
        return {"status": "error", "message": str(e)}


# ============================================================================
# Schedules
# ============================================================================

@mcp.tool()
async def list_recurring_schedules(adom: str = "root") -> dict[str, Any]:
    """List all recurring schedules in an ADOM.
    
    Recurring schedules are used for time-based firewall policies.
    
    Args:
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with schedules list
    """
    try:
        api = _get_advanced_objects_api()
        schedules = await api.list_schedules_recurring(adom=adom)
        return {
            "status": "success",
            "count": len(schedules),
            "schedules": schedules,
        }
    except Exception as e:
        logger.error(f"Error listing recurring schedules in ADOM {adom}: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def list_onetime_schedules(adom: str = "root") -> dict[str, Any]:
    """List all one-time schedules in an ADOM.
    
    Args:
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with schedules list
    """
    try:
        api = _get_advanced_objects_api()
        schedules = await api.list_schedules_onetime(adom=adom)
        return {
            "status": "success",
            "count": len(schedules),
            "schedules": schedules,
        }
    except Exception as e:
        logger.error(f"Error listing one-time schedules in ADOM {adom}: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def create_recurring_schedule(
    name: str,
    days: list[str],
    start_time: str,
    end_time: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Create a recurring schedule for time-based policies.
    
    Args:
        name: Schedule name
        days: List of days (e.g., ["monday", "tuesday", "wednesday"])
        start_time: Start time in HH:MM format (e.g., "08:00")
        end_time: End time in HH:MM format (e.g., "18:00")
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with creation result
        
    Example:
        # Create business hours schedule
        result = create_recurring_schedule(
            name="business-hours",
            days=["monday", "tuesday", "wednesday", "thursday", "friday"],
            start_time="08:00",
            end_time="18:00",
            adom="production"
        )
    """
    try:
        api = _get_advanced_objects_api()
        result = await api.create_schedule_recurring(
            name=name,
            day=days,
            start=start_time,
            end=end_time,
            adom=adom,
        )
        return {
            "status": "success",
            "message": f"Recurring schedule '{name}' created",
            "result": result,
        }
    except Exception as e:
        logger.error(f"Error creating recurring schedule '{name}': {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def delete_recurring_schedule(name: str, adom: str = "root") -> dict[str, Any]:
    """Delete a recurring schedule.
    
    Args:
        name: Schedule name
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with deletion result
    """
    try:
        api = _get_advanced_objects_api()
        result = await api.delete_schedule_recurring(name=name, adom=adom)
        return {
            "status": "success",
            "message": f"Recurring schedule '{name}' deleted successfully",
            "result": result,
        }
    except Exception as e:
        logger.error(f"Error deleting recurring schedule '{name}': {e}")
        return {"status": "error", "message": str(e)}


# ============================================================================
# Wildcard FQDNs
# ============================================================================

@mcp.tool()
async def list_wildcard_fqdns(adom: str = "root") -> dict[str, Any]:
    """List all wildcard FQDNs in an ADOM.
    
    Wildcard FQDNs allow pattern-based domain matching (e.g., *.example.com).
    
    Args:
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with wildcard FQDNs list
    """
    try:
        api = _get_advanced_objects_api()
        fqdns = await api.list_wildcard_fqdns(adom=adom)
        return {
            "status": "success",
            "count": len(fqdns),
            "wildcard_fqdns": fqdns,
        }
    except Exception as e:
        logger.error(f"Error listing wildcard FQDNs in ADOM {adom}: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def create_wildcard_fqdn(
    name: str,
    pattern: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Create a wildcard FQDN for pattern-based domain matching.
    
    Args:
        name: Object name
        pattern: Wildcard domain pattern (e.g., "*.google.com")
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with creation result
        
    Example:
        # Block all Google domains
        result = create_wildcard_fqdn(
            name="all-google-domains",
            pattern="*.google.com",
            adom="production"
        )
    """
    try:
        api = _get_advanced_objects_api()
        result = await api.create_wildcard_fqdn(
            name=name,
            wildcard_fqdn=pattern,
            adom=adom,
        )
        return {
            "status": "success",
            "message": f"Wildcard FQDN '{name}' created for pattern '{pattern}'",
            "result": result,
        }
    except Exception as e:
        logger.error(f"Error creating wildcard FQDN '{name}': {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def delete_wildcard_fqdn(name: str, adom: str = "root") -> dict[str, Any]:
    """Delete a wildcard FQDN.
    
    Args:
        name: Wildcard FQDN name
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with deletion result
    """
    try:
        api = _get_advanced_objects_api()
        result = await api.delete_wildcard_fqdn(name=name, adom=adom)
        return {
            "status": "success",
            "message": f"Wildcard FQDN '{name}' deleted successfully",
            "result": result,
        }
    except Exception as e:
        logger.error(f"Error deleting wildcard FQDN '{name}': {e}")
        return {"status": "error", "message": str(e)}

