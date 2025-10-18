"""Meta-tools for dynamic tool discovery and execution.

These tools are loaded in dynamic mode to enable tool discovery and on-demand execution
without loading all 590 tools into the context window.
"""

import logging
from typing import Any

from fortimanager_mcp.server import mcp
from fortimanager_mcp.utils.tool_registry import (
    execute_tool_dynamic,
    get_tool_categories,
    get_tool_metadata,
    search_tools,
)

logger = logging.getLogger(__name__)


@mcp.tool()
async def search_fortimanager_tools(
    query: str | None = None,
    category: str | None = None,
    limit: int = 20,
) -> dict[str, Any]:
    """Search for available FortiManager tools.

    Use this tool FIRST to discover which FortiManager operations are available.
    It searches through all 590 tools without loading them into your context.

    Once you find the tools you need, use execute_fortimanager_tool to run them.

    Args:
        query: Search term (e.g., "firewall address", "install policy", "device status")
               Searches in tool names and descriptions
        category: Filter by category (devices, objects, policies, monitoring, security,
                 provisioning, system, adom, vpn, sdwan, scripts, fortiguard, workspace)
        limit: Maximum number of results to return (default: 20)

    Returns:
        Dictionary with matching tools and their metadata

    Example:
        # Find tools for managing firewall addresses
        search_fortimanager_tools(query="firewall address")

        # Find all device management tools
        search_fortimanager_tools(category="devices")

        # Find policy installation tools
        search_fortimanager_tools(query="install policy")
    """
    try:
        results = search_tools(query=query, category=category, limit=limit)

        return {
            "status": "success",
            "count": len(results),
            "query": query,
            "category": category,
            "tools": [
                {
                    "name": tool.name,
                    "category": tool.category,
                    "description": tool.description,
                    "parameters": tool.parameters,
                    "requires_adom": tool.requires_adom,
                }
                for tool in results
            ],
            "tip": "Use execute_fortimanager_tool() to run any of these tools",
        }
    except Exception as e:
        logger.error(f"Error searching tools: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
def list_fortimanager_categories() -> dict[str, Any]:
    """List all FortiManager tool categories.

    Shows all available categories with descriptions and tool counts.
    Use this to understand the organization of the 590 FortiManager tools.

    Returns:
        Dictionary with all categories and their metadata

    Example:
        # See all available categories
        list_fortimanager_categories()

        # Then search within a category
        search_fortimanager_tools(category="devices")
    """
    try:
        categories = get_tool_categories()

        return {
            "status": "success",
            "total_tools": sum(cat["tool_count"] for cat in categories.values()),
            "categories": categories,
            "tip": "Use search_fortimanager_tools(category='...') to explore tools in a category",
        }
    except Exception as e:
        logger.error(f"Error listing categories: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def execute_fortimanager_tool(
    tool_name: str,
    **parameters: Any,
) -> dict[str, Any]:
    """Execute a FortiManager tool by name.

    This is the main tool for executing FortiManager operations in dynamic mode.
    First use search_fortimanager_tools() to discover available tools, then use
    this tool to execute them.

    Args:
        tool_name: Exact name of the tool to execute (from search results)
        **parameters: All parameters required by the tool

    Returns:
        Result from the executed tool

    Example:
        # First, search for the tool you need
        search_fortimanager_tools(query="list devices")
        # Returns: tool name "list_devices"

        # Then execute it
        execute_fortimanager_tool(
            tool_name="list_devices",
            adom="root"
        )

        # Another example: create a firewall address
        execute_fortimanager_tool(
            tool_name="create_firewall_address",
            name="internal_network",
            subnet="10.0.0.0/8",
            adom="root",
            comment="Internal network"
        )
    """
    try:
        # Get tool metadata first to validate
        metadata = get_tool_metadata(tool_name)
        if not metadata:
            available_tools = list(search_tools(limit=10))
            return {
                "status": "error",
                "message": f"Tool '{tool_name}' not found",
                "tip": "Use search_fortimanager_tools() to find available tools",
                "suggestions": [t.name for t in available_tools[:5]],
            }

        # Execute the tool
        logger.info(f"Executing tool '{tool_name}' with parameters: {parameters}")
        result = await execute_tool_dynamic(tool_name, **parameters)

        return result

    except Exception as e:
        logger.error(f"Error executing tool '{tool_name}': {e}")
        return {
            "status": "error",
            "message": str(e),
            "tool_name": tool_name,
            "parameters": parameters,
        }


@mcp.tool()
def get_fortimanager_tool_info(tool_name: str) -> dict[str, Any]:
    """Get detailed information about a specific FortiManager tool.

    Use this to see the full documentation, parameters, and usage examples
    for a tool before executing it.

    Args:
        tool_name: Name of the tool

    Returns:
        Detailed tool information including parameters and examples

    Example:
        # Get details about a specific tool
        get_fortimanager_tool_info("create_firewall_address")
    """
    try:
        metadata = get_tool_metadata(tool_name)
        if not metadata:
            return {
                "status": "error",
                "message": f"Tool '{tool_name}' not found",
                "tip": "Use search_fortimanager_tools() to find available tools",
            }

        return {
            "status": "success",
            "tool": {
                "name": metadata.name,
                "category": metadata.category,
                "description": metadata.description,
                "module": metadata.module,
                "parameters": metadata.parameters,
                "requires_adom": metadata.requires_adom,
            },
            "usage": f"execute_fortimanager_tool(tool_name='{tool_name}', ...parameters...)",
        }
    except Exception as e:
        logger.error(f"Error getting tool info for '{tool_name}': {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
def fortimanager_help() -> dict[str, Any]:
    """Get help on using FortiManager MCP tools in dynamic mode.

    This server is running in DYNAMIC mode, which means tools are loaded on-demand
    to save context window space. This help explains the workflow.

    Returns:
        Help information and workflow guide
    """
    return {
        "mode": "dynamic",
        "total_tools": "590 FortiManager tools available",
        "workflow": {
            "step_1": {
                "title": "Discover tools",
                "tools": [
                    "list_fortimanager_categories() - See all categories",
                    "search_fortimanager_tools(query='...') - Search for tools",
                ],
            },
            "step_2": {
                "title": "Get tool details",
                "tools": ["get_fortimanager_tool_info(tool_name='...') - See parameters"],
            },
            "step_3": {
                "title": "Execute tool",
                "tools": ["execute_fortimanager_tool(tool_name='...', **params) - Run the tool"],
            },
        },
        "examples": [
            {
                "task": "List all devices",
                "steps": [
                    "1. search_fortimanager_tools(query='list devices')",
                    "2. execute_fortimanager_tool(tool_name='list_devices', adom='root')",
                ],
            },
            {
                "task": "Create firewall address",
                "steps": [
                    "1. search_fortimanager_tools(query='firewall address', category='objects')",
                    "2. get_fortimanager_tool_info('create_firewall_address')",
                    "3. execute_fortimanager_tool(tool_name='create_firewall_address', name='test', subnet='10.0.0.0/24', adom='root')",
                ],
            },
        ],
        "categories": [
            "devices - Device management",
            "objects - Firewall objects",
            "policies - Policy management",
            "monitoring - System monitoring",
            "security - Security profiles",
            "provisioning - Templates and provisioning",
            "system - System administration",
            "adom - ADOM management",
            "vpn - VPN management",
            "sdwan - SD-WAN configuration",
            "scripts - CLI script management",
            "fortiguard - FortiGuard updates",
            "workspace - Workspace locking",
        ],
        "tip": "Start with list_fortimanager_categories() or search_fortimanager_tools(query='your task')",
    }

