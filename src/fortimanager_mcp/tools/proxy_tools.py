"""Direct proxy tools for common FortiManager operations.

These tools provide a natural, direct interface for LLMs in dynamic mode.
Each tool directly calls the underlying FortiManager operation without
requiring search/discovery steps.
"""

import logging
from typing import Any

from fortimanager_mcp.server import mcp, settings
from fortimanager_mcp.utils.tool_registry import execute_tool_dynamic

logger = logging.getLogger(__name__)

# Determine which tools to register based on mode
IS_DYNAMIC_MODE = settings.FMG_TOOL_MODE == "dynamic"


def conditional_tool(discovery_only: bool = False):
    """Conditionally apply @mcp.tool() decorator based on mode.

    Args:
        discovery_only: If True, only register in dynamic mode. If False, register in both modes.
    """
    def decorator(func):
        if not discovery_only or IS_DYNAMIC_MODE:
            return mcp.tool()(func)
        else:
            return func
    return decorator


# ============================================================================
# ADOM Management - Direct Tools
# ============================================================================

@mcp.tool()
async def list_adoms() -> dict[str, Any]:
    """List all Administrative Domains (ADOMs) in FortiManager.

    Returns all configured ADOMs with their status, version, and settings.

    Returns:
        Dictionary with list of ADOMs and their details

    Example:
        "Show me all ADOMs" → list_adoms()
        "What ADOMs exist?" → list_adoms()
    """
    return await execute_tool_dynamic("list_adoms")


@mcp.tool()
async def get_adom_details(adom: str) -> dict[str, Any]:
    """Get detailed statistics and information about a specific ADOM.
    
    Shows comprehensive information including device count, policy count, 
    object statistics, and health status for the specified ADOM.
    
    Args:
        adom: ADOM name
        
    Returns:
        Dictionary with ADOM details and statistics
        
    Example:
        "Tell me about the root ADOM" → get_adom_details(adom="root")
    """
    return await execute_tool_dynamic("get_adom_statistics", adom=adom)


# ============================================================================
# Device Management - Direct Tools
# ============================================================================

@mcp.tool()
async def list_devices(adom: str | None = None) -> dict[str, Any]:
    """List all managed FortiGate devices.
    
    Shows all devices with their connection status, IP, version, and platform.
    
    Args:
        adom: Optional ADOM name to filter devices
        
    Returns:
        Dictionary with list of devices
        
    Example:
        "Show all devices" → list_devices()
        "List devices in root ADOM" → list_devices(adom="root")
    """
    return await execute_tool_dynamic("list_devices", adom=adom)


@mcp.tool()
async def get_device_details(name: str, adom: str | None = None) -> dict[str, Any]:
    """Get detailed information about a specific FortiGate device.
    
    Args:
        name: Device name
        adom: Optional ADOM name
        
    Returns:
        Dictionary with device details
        
    Example:
        "Tell me about device FGT-001" → get_device_details(name="FGT-001")
    """
    return await execute_tool_dynamic("get_device_details", name=name, adom=adom)


# ============================================================================
# Firewall Objects - Direct Tools
# ============================================================================

@mcp.tool()
async def list_firewall_addresses(
    adom: str = "root",
    filter_name: str | None = None,
) -> dict[str, Any]:
    """List firewall address objects in an ADOM.
    
    Args:
        adom: ADOM name (default: "root")
        filter_name: Optional name filter
        
    Returns:
        Dictionary with list of addresses
        
    Example:
        "Show firewall addresses" → list_firewall_addresses()
        "List addresses in production" → list_firewall_addresses(adom="production")
    """
    return await execute_tool_dynamic(
        "list_firewall_addresses",
        adom=adom,
        filter_name=filter_name,
    )


@mcp.tool()
async def create_firewall_address(
    name: str,
    subnet: str,
    adom: str = "root",
    comment: str | None = None,
) -> dict[str, Any]:
    """Create a new firewall address object.
    
    Args:
        name: Address name
        subnet: IP subnet in CIDR format (e.g., "10.0.0.0/24")
        adom: ADOM name (default: "root")
        comment: Optional description
        
    Returns:
        Dictionary with created address details
        
    Example:
        "Create address internal_net 10.0.0.0/8" →
        create_firewall_address(name="internal_net", subnet="10.0.0.0/8")
    """
    return await execute_tool_dynamic(
        "create_firewall_address",
        name=name,
        subnet=subnet,
        adom=adom,
        comment=comment,
    )


# ============================================================================
# Policy Management - Direct Tools
# ============================================================================

@mcp.tool()
async def list_policy_packages(adom: str = "root") -> dict[str, Any]:
    """List all policy packages in an ADOM.
    
    Args:
        adom: ADOM name (default: "root")
        
    Returns:
        Dictionary with list of policy packages
        
    Example:
        "Show policy packages" → list_policy_packages()
        "List packages in production" → list_policy_packages(adom="production")
    """
    return await execute_tool_dynamic("list_policy_packages", adom=adom)


@mcp.tool()
async def list_firewall_policies(
    adom: str,
    package: str,
) -> dict[str, Any]:
    """List firewall policies in a policy package.
    
    Args:
        adom: ADOM name
        package: Policy package name
        
    Returns:
        Dictionary with list of policies
        
    Example:
        "Show policies in default package" →
        list_firewall_policies(adom="root", package="default")
    """
    return await execute_tool_dynamic(
        "list_firewall_policies",
        adom=adom,
        package=package,
    )


# ============================================================================
# System Monitoring - Direct Tools
# ============================================================================

@mcp.tool()
async def get_system_status() -> dict[str, Any]:
    """Get FortiManager system status.
    
    Returns system information including version, hostname, and uptime.
    
    Returns:
        Dictionary with system status
        
    Example:
        "What's the system status?" → get_system_status()
        "Show FortiManager info" → get_system_status()
    """
    return await execute_tool_dynamic("get_system_status")


@mcp.tool()
async def list_tasks(limit: int | None = None) -> dict[str, Any]:
    """List recent FortiManager tasks.
    
    Shows recent system tasks with their status and progress.
    
    Args:
        limit: Maximum number of tasks to return
        
    Returns:
        Dictionary with list of tasks
        
    Example:
        "Show recent tasks" → list_tasks()
        "List last 10 tasks" → list_tasks(limit=10)
    """
    return await execute_tool_dynamic("list_tasks", limit=limit)


# ============================================================================
# Discovery Tool - For Less Common Operations
# ============================================================================

@mcp.tool()
async def find_fortimanager_tool(operation: str) -> dict[str, Any]:
    """Find the right FortiManager tool for an operation.
    
    Use this when you need to perform an operation that doesn't have a direct tool.
    This searches all 590 available operations and shows you how to execute them.
    
    Args:
        operation: What you want to do (e.g., "create VPN tunnel", "backup config")
        
    Returns:
        Dictionary with matching tools and execution instructions
        
    Example:
        "How do I create a VPN?" → find_fortimanager_tool(operation="create VPN")
        "Need to backup system" → find_fortimanager_tool(operation="backup")
    """
    from fortimanager_mcp.utils.tool_registry import search_tools
    
    results = search_tools(query=operation, limit=5)
    
    if not results:
        return {
            "status": "not_found",
            "message": f"No tools found for '{operation}'",
            "suggestion": "Try different keywords or use list_fortimanager_categories() to browse",
        }
    
    return {
        "status": "success",
        "operation": operation,
        "found": len(results),
        "tools": [
            {
                "name": tool.name,
                "category": tool.category,
                "description": tool.description,
                "how_to_use": f"execute_advanced_tool(tool_name='{tool.name}', ...parameters...)",
                "parameters": tool.parameters,
            }
            for tool in results
        ],
        "note": "Use execute_advanced_tool() to run these tools",
    }


@mcp.tool()
async def execute_advanced_tool(tool_name: str, **parameters: Any) -> dict[str, Any]:
    """Execute an advanced FortiManager operation.
    
    Use this to run operations that don't have direct tools above.
    First use find_fortimanager_tool() to discover the tool name.
    
    Args:
        tool_name: Exact tool name from find_fortimanager_tool()
        **parameters: Tool-specific parameters
        
    Returns:
        Result from the executed tool
        
    Example:
        # First find the tool
        find_fortimanager_tool(operation="create VPN tunnel")
        
        # Then execute it
        execute_advanced_tool(
            tool_name="create_vpn_ipsec_phase1",
            name="my_vpn",
            remote_gw="1.2.3.4",
            ...
        )
    """
    return await execute_tool_dynamic(tool_name, **parameters)


@mcp.tool()
def list_fortimanager_categories() -> dict[str, Any]:
    """List all FortiManager operation categories.
    
    Shows the 15 categories organizing all 590 operations.
    
    Returns:
        Dictionary with categories and tool counts
        
    Example:
        "What operations are available?" → list_fortimanager_categories()
    """
    from fortimanager_mcp.utils.tool_registry import get_tool_categories
    
    categories = get_tool_categories()
    
    return {
        "status": "success",
        "total_operations": sum(cat["tool_count"] for cat in categories.values()),
        "categories": categories,
        "note": "Use find_fortimanager_tool() to discover operations in each category",
    }

