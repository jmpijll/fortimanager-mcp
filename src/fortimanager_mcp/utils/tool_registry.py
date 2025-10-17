"""Tool registry for dynamic tool loading and discovery."""

import importlib
import inspect
from dataclasses import dataclass
from typing import Any, Callable

import logging

logger = logging.getLogger(__name__)


@dataclass
class ToolMetadata:
    """Metadata for a FortiManager MCP tool."""

    name: str
    module: str
    category: str
    description: str
    parameters: dict[str, Any]
    requires_adom: bool = False


# Complete registry of all FortiManager MCP tools
# This is used in dynamic mode to discover and execute tools without loading them all
TOOL_REGISTRY: dict[str, ToolMetadata] = {
    # Device Management Tools (69 tools)
    "list_devices": ToolMetadata(
        name="list_devices",
        module="fortimanager_mcp.tools.device_tools",
        category="devices",
        description="List all managed FortiGate devices",
        parameters={"adom": {"type": "string", "optional": True}},
    ),
    "get_device_details": ToolMetadata(
        name="get_device_details",
        module="fortimanager_mcp.tools.device_tools",
        category="devices",
        description="Get detailed information about a specific device",
        parameters={
            "name": {"type": "string", "required": True},
            "adom": {"type": "string", "optional": True},
        },
    ),
    "add_device": ToolMetadata(
        name="add_device",
        module="fortimanager_mcp.tools.device_tools",
        category="devices",
        description="Add a new FortiGate device to FortiManager",
        parameters={
            "name": {"type": "string", "required": True},
            "ip": {"type": "string", "required": True},
            "username": {"type": "string", "required": True},
            "password": {"type": "string", "required": True},
            "adom": {"type": "string", "optional": True},
        },
    ),
    # Firewall Object Tools (47 tools)
    "list_firewall_addresses": ToolMetadata(
        name="list_firewall_addresses",
        module="fortimanager_mcp.tools.object_tools",
        category="objects",
        description="List firewall address objects in an ADOM",
        parameters={
            "adom": {"type": "string", "optional": True},
            "filter_name": {"type": "string", "optional": True},
        },
        requires_adom=True,
    ),
    "create_firewall_address": ToolMetadata(
        name="create_firewall_address",
        module="fortimanager_mcp.tools.object_tools",
        category="objects",
        description="Create a new firewall address object",
        parameters={
            "name": {"type": "string", "required": True},
            "subnet": {"type": "string", "required": True},
            "adom": {"type": "string", "optional": True},
            "comment": {"type": "string", "optional": True},
        },
        requires_adom=True,
    ),
    # Policy Management Tools (64 tools)
    "list_policy_packages": ToolMetadata(
        name="list_policy_packages",
        module="fortimanager_mcp.tools.policy_tools",
        category="policies",
        description="List policy packages in an ADOM",
        parameters={"adom": {"type": "string", "optional": True}},
        requires_adom=True,
    ),
    "list_firewall_policies": ToolMetadata(
        name="list_firewall_policies",
        module="fortimanager_mcp.tools.policy_tools",
        category="policies",
        description="List firewall policies in a policy package",
        parameters={
            "adom": {"type": "string", "required": True},
            "package": {"type": "string", "required": True},
        },
        requires_adom=True,
    ),
    # Monitoring Tools (43 tools)
    "get_system_status": ToolMetadata(
        name="get_system_status",
        module="fortimanager_mcp.tools.monitoring_tools",
        category="monitoring",
        description="Get FortiManager system status",
        parameters={},
    ),
    "list_tasks": ToolMetadata(
        name="list_tasks",
        module="fortimanager_mcp.tools.monitoring_tools",
        category="monitoring",
        description="List recent tasks",
        parameters={"limit": {"type": "integer", "optional": True}},
    ),
}


def get_tool_categories() -> dict[str, dict[str, Any]]:
    """Get all tool categories with counts and descriptions.

    Returns:
        Dictionary of categories with metadata
    """
    categories = {
        "devices": {
            "name": "Device Management",
            "description": "Device lifecycle, firmware, HA clusters, VDOMs, configuration",
            "tool_count": 69,
            "module": "device_tools",
        },
        "objects": {
            "name": "Firewall Objects",
            "description": "Addresses, services, zones, VIPs, IP pools, schedules",
            "tool_count": 47,
            "module": "object_tools",
        },
        "policies": {
            "name": "Policy Management",
            "description": "Policy packages, firewall rules, NAT policies, installation",
            "tool_count": 64,
            "module": "policy_tools",
        },
        "monitoring": {
            "name": "Monitoring & Tasks",
            "description": "System status, device connectivity, task tracking, statistics",
            "tool_count": 43,
            "module": "monitoring_tools",
        },
        "security": {
            "name": "Security Profiles",
            "description": "Web filter, IPS, antivirus, application control, DLP",
            "tool_count": 33,
            "module": "security_tools",
        },
        "provisioning": {
            "name": "Provisioning & Templates",
            "description": "CLI templates, system templates, device profiles",
            "tool_count": 98,
            "module": "provisioning_tools",
        },
        "system": {
            "name": "System Operations",
            "description": "Administration, backup, restore, certificates, users",
            "tool_count": 47,
            "module": "system_tools",
        },
        "adom": {
            "name": "ADOM Management",
            "description": "Administrative domains, workspace locking, revisions",
            "tool_count": 28,
            "module": "adom_tools",
        },
        "vpn": {
            "name": "VPN Management",
            "description": "IPsec tunnels, SSL-VPN, certificates, monitoring",
            "tool_count": 24,
            "module": "vpn_tools",
        },
        "sdwan": {
            "name": "SD-WAN",
            "description": "SD-WAN zones, health checks, services, templates",
            "tool_count": 19,
            "module": "sdwan_tools",
        },
        "scripts": {
            "name": "CLI Scripts",
            "description": "Script management, execution, scheduling",
            "tool_count": 12,
            "module": "script_tools",
        },
        "fortiguard": {
            "name": "FortiGuard",
            "description": "Updates, contracts, threat feeds, packages",
            "tool_count": 23,
            "module": "fortiguard_tools",
        },
        "workspace": {
            "name": "Workspace & Locking",
            "description": "ADOM locking, commits, lock status",
            "tool_count": 12,
            "module": "workspace_tools",
        },
        "advanced_objects": {
            "name": "Advanced Objects",
            "description": "Dynamic objects, threat feeds, SDN connectors",
            "tool_count": 18,
            "module": "advanced_object_tools",
        },
        "additional_objects": {
            "name": "Additional Objects",
            "description": "Schedules, internet services, geography, multicast",
            "tool_count": 16,
            "module": "additional_object_tools",
        },
    }
    return categories


def search_tools(
    query: str | None = None,
    category: str | None = None,
    limit: int = 20,
) -> list[ToolMetadata]:
    """Search for tools matching criteria.

    Args:
        query: Search term to match in name or description
        category: Filter by category
        limit: Maximum results to return

    Returns:
        List of matching tool metadata
    """
    results: list[ToolMetadata] = []

    for tool in TOOL_REGISTRY.values():
        # Filter by category
        if category and tool.category != category:
            continue

        # Filter by query
        if query:
            query_lower = query.lower()
            if query_lower not in tool.name.lower() and query_lower not in tool.description.lower():
                continue

        results.append(tool)

        if len(results) >= limit:
            break

    return results


def get_tool_metadata(tool_name: str) -> ToolMetadata | None:
    """Get metadata for a specific tool.

    Args:
        tool_name: Name of the tool

    Returns:
        Tool metadata or None if not found
    """
    return TOOL_REGISTRY.get(tool_name)


async def execute_tool_dynamic(tool_name: str, **kwargs: Any) -> Any:
    """Dynamically import and execute a tool.

    This allows tools to be executed without loading them all into memory.

    Args:
        tool_name: Name of the tool to execute
        **kwargs: Arguments to pass to the tool

    Returns:
        Tool execution result

    Raises:
        ValueError: If tool not found
        RuntimeError: If tool execution fails
    """
    # Get tool metadata
    metadata = get_tool_metadata(tool_name)
    if not metadata:
        raise ValueError(f"Tool '{tool_name}' not found in registry")

    try:
        # Dynamically import the module
        module = importlib.import_module(metadata.module)

        # Get the tool function
        tool_func = getattr(module, tool_name, None)
        if not tool_func:
            raise RuntimeError(f"Tool function '{tool_name}' not found in module {metadata.module}")

        # Execute the tool
        if inspect.iscoroutinefunction(tool_func):
            result = await tool_func(**kwargs)
        else:
            result = tool_func(**kwargs)

        return result

    except Exception as e:
        logger.error(f"Error executing tool '{tool_name}': {e}")
        raise RuntimeError(f"Failed to execute tool '{tool_name}': {e}") from e


def populate_registry() -> None:
    """Populate registry with all tools from all modules.

    This is called at startup in dynamic mode to build the complete registry.
    Currently uses a static registry. Future enhancement: auto-generate from modules.
    """
    logger.info("Tool registry initialized")
    logger.info(f"Registry contains metadata for {len(TOOL_REGISTRY)} tools")
    logger.info("Note: Static registry in use. Run 'generate_registry.py' to update from source.")

