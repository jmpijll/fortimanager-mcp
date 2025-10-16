"""Cyber Security Fabric MCP Tools."""

import logging
from typing import Any

from fortimanager_mcp.api.csf import CSFAPI
from fortimanager_mcp.server import get_fmg_client, mcp

logger = logging.getLogger(__name__)


def _get_csf_api() -> CSFAPI:
    client = get_fmg_client()
    if not client:
        raise RuntimeError("FortiManager client not initialized")
    return CSFAPI(client)


# =============================================================================
# Phase 33: Cyber Security Fabric (CSF)
# =============================================================================


@mcp.tool()
async def get_fabric_topology(adom: str = "root") -> dict[str, Any]:
    """Get Security Fabric topology and device relationships.
    
    The Security Fabric creates a unified security architecture by connecting
    multiple FortiGate devices. This tool retrieves the topology showing:
    - Root FortiGate (fabric leader)
    - Downstream FortiGates (fabric members)
    - Device relationships and trust status
    - Fabric communication paths
    
    Use this to:
    - Visualize security fabric architecture
    - Verify fabric connectivity
    - Troubleshoot fabric issues
    - Document network topology
    
    Args:
        adom: ADOM name (default: "root")
    
    Returns:
        Dictionary with fabric topology information
    
    Example:
        result = get_fabric_topology(adom="root")
        # Returns complete fabric topology with all devices
    """
    try:
        api = _get_csf_api()
        topology = await api.get_fabric_topology(adom=adom)
        return {
            "status": "success",
            "topology": topology,
        }
    except Exception as e:
        logger.error(f"Error getting fabric topology: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def list_fabric_devices(adom: str = "root") -> dict[str, Any]:
    """List all devices in the Security Fabric.
    
    Shows all FortiGate devices participating in the Security Fabric including:
    - **Root FortiGate**: Primary device managing the fabric
    - **Downstream FortiGates**: Member devices in the fabric
    - Device roles and capabilities
    - Connection status
    
    The Security Fabric enables:
    - Unified threat intelligence sharing
    - Coordinated security policy enforcement
    - Centralized visibility across all devices
    - Automated threat response
    
    Args:
        adom: ADOM name (default: "root")
    
    Returns:
        Dictionary with list of fabric devices
    
    Example:
        result = list_fabric_devices(adom="root")
        # Returns all fabric-connected FortiGates
    """
    try:
        api = _get_csf_api()
        devices = await api.list_fabric_devices(adom=adom)
        return {
            "status": "success",
            "count": len(devices),
            "devices": devices,
        }
    except Exception as e:
        logger.error(f"Error listing fabric devices: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_fabric_authorization_status(
    device_name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Get fabric authorization status for a device.
    
    Checks whether a device is authorized to join the Security Fabric.
    Authorization is required to establish trust between devices.
    
    Status indicators:
    - **Authorized**: Device can participate in fabric
    - **Pending**: Awaiting administrator approval
    - **Denied**: Device blocked from joining
    
    Args:
        device_name: Device name to check
        adom: ADOM name (default: "root")
    
    Returns:
        Dictionary with authorization status
    
    Example:
        result = get_fabric_authorization_status(
            device_name="FGT-Branch-01",
            adom="root"
        )
    """
    try:
        api = _get_csf_api()
        status = await api.get_fabric_authorization_status(
            device_name=device_name,
            adom=adom,
        )
        return {
            "status": "success",
            "device": device_name,
            "authorization": status,
        }
    except Exception as e:
        logger.error(f"Error getting fabric authorization status: {e}")
        return {"status": "error", "message": str(e)}


