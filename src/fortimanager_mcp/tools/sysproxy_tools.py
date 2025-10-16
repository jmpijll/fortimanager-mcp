"""MCP tools for system proxy JSON operations."""

import logging
from typing import Any

from fortimanager_mcp.api.sysproxy import SysProxyAPI
from fortimanager_mcp.server import get_fmg_client, mcp

logger = logging.getLogger(__name__)


def _get_sysproxy_api() -> SysProxyAPI:
    """Get SysProxyAPI instance."""
    client = get_fmg_client()
    if not client:
        raise RuntimeError("FortiManager client not initialized")
    return SysProxyAPI(client)


@mcp.tool()
async def execute_device_json_commands(
    device_name: str,
    commands: list[str],
    adom: str = "root",
) -> dict[str, Any]:
    """Execute JSON-RPC commands on a managed device via system proxy.

    Allows direct execution of FortiGate JSON-RPC API commands through FortiManager.
    More flexible than CLI commands for advanced automation.

    Args:
        device_name: Target device name
        commands: List of JSON-RPC commands to execute
        adom: ADOM name (default: root)

    Returns:
        Dictionary with command execution results
    """
    try:
        api = _get_sysproxy_api()
        result = await api.execute_proxy_json(device_name=device_name, commands=commands, adom=adom)
        return {
            "status": "success",
            "device": device_name,
            "command_count": len(commands),
            "results": result,
        }
    except Exception as e:
        logger.error(f"Error executing JSON commands: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_device_proxy_capabilities(device_name: str, adom: str = "root") -> dict[str, Any]:
    """Get proxy capabilities and supported operations for a managed device.

    Retrieves information about what proxy operations are supported by the device.

    Args:
        device_name: Target device name
        adom: ADOM name (default: root)

    Returns:
        Dictionary with proxy capabilities
    """
    try:
        api = _get_sysproxy_api()
        capabilities = await api.get_proxy_capabilities(device_name=device_name, adom=adom)
        return {"status": "success", "device": device_name, "capabilities": capabilities}
    except Exception as e:
        logger.error(f"Error getting proxy capabilities: {e}")
        return {"status": "error", "message": str(e)}


