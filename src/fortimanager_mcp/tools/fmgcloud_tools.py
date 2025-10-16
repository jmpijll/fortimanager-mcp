"""FortiManager Cloud MCP Tools."""

import logging
from typing import Any

from fortimanager_mcp.api.fmgcloud import FMGCloudAPI
from fortimanager_mcp.server import get_fmg_client, mcp

logger = logging.getLogger(__name__)


def _get_fmgcloud_api() -> FMGCloudAPI:
    client = get_fmg_client()
    if not client:
        raise RuntimeError("FortiManager client not initialized")
    return FMGCloudAPI(client)


# =============================================================================
# Phase 35: FortiManager Cloud Operations
# =============================================================================


@mcp.tool()
async def get_cloud_service_status() -> dict[str, Any]:
    """Get FortiManager cloud service status and connectivity.
    
    Retrieves status of FortiCloud integration including:
    - **Cloud connectivity**: Connection state to FortiCloud
    - **Service availability**: Status of cloud services
    - **Subscription status**: Active/expired subscription info
    - **Last sync time**: When data was last synchronized
    
    FortiCloud services provide:
    - Cloud-based management and monitoring
    - Configuration backup and restore
    - Threat intelligence updates
    - Compliance reporting
    - Remote access capabilities
    
    Returns:
        Dictionary with cloud service status
    
    Example:
        result = get_cloud_service_status()
        # Returns connection state, subscription info
    """
    try:
        api = _get_fmgcloud_api()
        status = await api.get_cloud_service_status()
        return {
            "status": "success",
            "cloud_status": status,
        }
    except Exception as e:
        logger.error(f"Error getting cloud service status: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_cloud_account_info() -> dict[str, Any]:
    """Get FortiCloud account information and subscription details.
    
    Retrieves FortiCloud account details including:
    - Account ID and email
    - Subscription type and tier
    - License information
    - Service entitlements
    - Expiration dates
    
    Use this to:
    - Verify subscription status
    - Check available services
    - Monitor license expiration
    - Audit cloud entitlements
    
    Returns:
        Dictionary with cloud account information
    
    Example:
        result = get_cloud_account_info()
        # Returns account ID, subscription type, license info
    """
    try:
        api = _get_fmgcloud_api()
        account_info = await api.get_cloud_account_info()
        return {
            "status": "success",
            "account": account_info,
        }
    except Exception as e:
        logger.error(f"Error getting cloud account info: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def sync_with_forticloud() -> dict[str, Any]:
    """Synchronize FortiManager with FortiCloud services.
    
    Triggers immediate synchronization of:
    - Configuration backups
    - Device inventory
    - Policy changes
    - Security events
    - License updates
    
    Synchronization enables:
    - Cloud-based disaster recovery
    - Multi-site management
    - Centralized reporting
    - Remote troubleshooting
    
    Returns:
        Dictionary with sync operation result
    
    Example:
        result = sync_with_forticloud()
        # Initiates cloud sync and returns task info
    """
    try:
        api = _get_fmgcloud_api()
        sync_result = await api.sync_with_cloud()
        return {
            "status": "success",
            "message": "Cloud synchronization initiated",
            "sync_result": sync_result,
        }
    except Exception as e:
        logger.error(f"Error syncing with FortiCloud: {e}")
        return {"status": "error", "message": str(e)}


