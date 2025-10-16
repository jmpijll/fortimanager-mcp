"""MCP tools for QoS management operations."""

import logging
from typing import Any

from fortimanager_mcp.api.qos import QoSAPI
from fortimanager_mcp.server import get_fmg_client, mcp

logger = logging.getLogger(__name__)


def _get_qos_api() -> QoSAPI:
    """Get QoSAPI instance."""
    client = get_fmg_client()
    if not client:
        raise RuntimeError("FortiManager client not initialized")
    return QoSAPI(client)


@mcp.tool()
async def list_qos_shaping_policies(adom: str = "root") -> dict[str, Any]:
    """List QoS traffic shaping policies.

    QoS policies control bandwidth allocation and traffic prioritization
    to ensure critical applications receive adequate network resources.

    Args:
        adom: ADOM name (default: root)

    Returns:
        Dictionary with list of QoS shaping policies
    """
    try:
        api = _get_qos_api()
        policies = await api.list_qos_policies(adom=adom)
        return {"status": "success", "count": len(policies), "policies": policies}
    except Exception as e:
        logger.error(f"Error listing QoS policies: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_device_qos_statistics(device_name: str, adom: str = "root") -> dict[str, Any]:
    """Get QoS statistics for a managed device.

    Retrieves real-time QoS statistics including bandwidth usage,
    traffic shaping effectiveness, and policy hit counts.

    Args:
        device_name: Target device name
        adom: ADOM name (default: root)

    Returns:
        Dictionary with QoS statistics
    """
    try:
        api = _get_qos_api()
        stats = await api.get_qos_statistics(device_name=device_name, adom=adom)
        return {"status": "success", "device": device_name, "qos_stats": stats}
    except Exception as e:
        logger.error(f"Error getting QoS statistics: {e}")
        return {"status": "error", "message": str(e)}

