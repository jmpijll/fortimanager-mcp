"""Connector Management MCP Tools."""

import logging
from typing import Any

from fortimanager_mcp.api.connectors import ConnectorAPI
from fortimanager_mcp.server import get_fmg_client, mcp

logger = logging.getLogger(__name__)


def _get_connector_api() -> ConnectorAPI:
    client = get_fmg_client()
    if not client:
        raise RuntimeError("FortiManager client not initialized")
    return ConnectorAPI(client)


# =============================================================================
# Phase 31: SDN Connectors
# =============================================================================


@mcp.tool()
async def list_sdn_connectors(adom: str = "root") -> dict[str, Any]:
    """List SDN (Software-Defined Networking) connectors.
    
    SDN connectors dynamically sync network objects from cloud platforms:
    - **AWS**: EC2 instances, VPCs, subnets, security groups
    - **Azure**: Virtual machines, VNets, resource groups
    - **GCP**: Compute instances, VPCs, firewall rules
    - **VMware NSX/vCenter**: Virtual machines, port groups
    - **OpenStack/Kubernetes**: Containers, pods, services
    
    Enables dynamic address objects that auto-update with cloud changes.
    
    Args:
        adom: ADOM name (default: "root")
    
    Returns:
        Dictionary with list of SDN connectors
    
    Example:
        result = list_sdn_connectors(adom="root")
    """
    try:
        api = _get_connector_api()
        connectors = await api.list_sdn_connectors(adom=adom)
        return {
            "status": "success",
            "count": len(connectors),
            "connectors": connectors,
        }
    except Exception as e:
        logger.error(f"Error listing SDN connectors: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_sdn_connector(name: str, adom: str = "root") -> dict[str, Any]:
    """Get SDN connector details and configuration.
    
    Retrieves complete configuration of an SDN connector including:
    - Connection credentials and endpoints
    - Sync schedule and status
    - Mapped network objects
    - Region/zone filters
    
    Args:
        name: SDN connector name
        adom: ADOM name (default: "root")
    
    Returns:
        Dictionary with connector configuration
    
    Example:
        result = get_sdn_connector(name="AWS-Prod", adom="root")
    """
    try:
        api = _get_connector_api()
        connector = await api.get_sdn_connector(name=name, adom=adom)
        return {
            "status": "success",
            "connector": connector,
        }
    except Exception as e:
        logger.error(f"Error getting SDN connector: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def refresh_sdn_connector(name: str, adom: str = "root") -> dict[str, Any]:
    """Manually refresh SDN connector to sync latest cloud resources.
    
    Triggers immediate synchronization with the cloud platform to:
    - Update dynamic address objects
    - Discover new instances/VMs
    - Remove terminated resources
    - Refresh network topology
    
    Use this after making cloud changes that need immediate reflection.
    
    Args:
        name: SDN connector name
        adom: ADOM name (default: "root")
    
    Returns:
        Dictionary with refresh result
    
    Example:
        result = refresh_sdn_connector(name="AWS-Prod", adom="root")
    """
    try:
        api = _get_connector_api()
        result = await api.refresh_sdn_connector(name=name, adom=adom)
        return {
            "status": "success",
            "message": f"SDN connector '{name}' refreshed",
            "result": result,
        }
    except Exception as e:
        logger.error(f"Error refreshing SDN connector: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_sdn_connector_status(name: str, adom: str = "root") -> dict[str, Any]:
    """Get SDN connector connection status and health.
    
    Shows real-time status including:
    - Connection state (connected/disconnected)
    - Last successful sync timestamp
    - Error messages if any
    - Number of synced objects
    
    Args:
        name: SDN connector name
        adom: ADOM name (default: "root")
    
    Returns:
        Dictionary with connector status
    
    Example:
        result = get_sdn_connector_status(name="Azure-Prod", adom="root")
    """
    try:
        api = _get_connector_api()
        status = await api.get_sdn_connector_status(name=name, adom=adom)
        return {
            "status": "success",
            "connector_status": status,
        }
    except Exception as e:
        logger.error(f"Error getting SDN connector status: {e}")
        return {"status": "error", "message": str(e)}


# =============================================================================
# Phase 31: Cloud & Fabric Connectors
# =============================================================================


@mcp.tool()
async def list_cloud_connectors(adom: str = "root") -> dict[str, Any]:
    """List cloud platform connectors.
    
    Cloud connectors integrate with cloud security services for:
    - Cloud-native security posture management
    - Threat intelligence sharing
    - Automated response and remediation
    
    Args:
        adom: ADOM name (default: "root")
    
    Returns:
        Dictionary with list of cloud connectors
    
    Example:
        result = list_cloud_connectors(adom="root")
    """
    try:
        api = _get_connector_api()
        connectors = await api.list_cloud_connectors(adom=adom)
        return {
            "status": "success",
            "count": len(connectors),
            "connectors": connectors,
        }
    except Exception as e:
        logger.error(f"Error listing cloud connectors: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_cloud_connector_services(
    connector_name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Get cloud services available through a cloud connector.
    
    Lists integrated cloud security services and their status.
    
    Args:
        connector_name: Cloud connector name
        adom: ADOM name (default: "root")
    
    Returns:
        Dictionary with available services
    
    Example:
        result = get_cloud_connector_services(
            connector_name="Cloud-Security",
            adom="root"
        )
    """
    try:
        api = _get_connector_api()
        services = await api.get_cloud_connector_services(
            connector_name=connector_name,
            adom=adom,
        )
        return {
            "status": "success",
            "services": services,
        }
    except Exception as e:
        logger.error(f"Error getting cloud connector services: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def list_fabric_connectors(adom: str = "root") -> dict[str, Any]:
    """List Security Fabric connectors.
    
    Fabric connectors integrate with Fortinet Security Fabric ecosystem:
    - **FortiAnalyzer**: Centralized logging and analytics
    - **FortiSandbox**: Advanced threat detection and sandboxing
    - **FortiWeb**: Web application firewall integration
    - **FortiMail**: Email security integration
    - **Third-party tools**: SIEM, ticketing, orchestration
    
    Args:
        adom: ADOM name (default: "root")
    
    Returns:
        Dictionary with list of Fabric connectors
    
    Example:
        result = list_fabric_connectors(adom="root")
    """
    try:
        api = _get_connector_api()
        connectors = await api.list_fabric_connectors(adom=adom)
        return {
            "status": "success",
            "count": len(connectors),
            "connectors": connectors,
        }
    except Exception as e:
        logger.error(f"Error listing Fabric connectors: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_fabric_connector_devices(
    connector_name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Get devices discovered through a Security Fabric connector.
    
    Shows devices and security tools integrated via the Fabric connector.
    
    Args:
        connector_name: Fabric connector name
        adom: ADOM name (default: "root")
    
    Returns:
        Dictionary with discovered devices
    
    Example:
        result = get_fabric_connector_devices(
            connector_name="Fabric-Main",
            adom="root"
        )
    """
    try:
        api = _get_connector_api()
        devices = await api.get_fabric_connector_devices(
            connector_name=connector_name,
            adom=adom,
        )
        return {
            "status": "success",
            "devices": devices,
        }
    except Exception as e:
        logger.error(f"Error getting Fabric connector devices: {e}")
        return {"status": "error", "message": str(e)}


# =============================================================================
# Phase 31: Connector Operations
# =============================================================================


@mcp.tool()
async def test_connector_connectivity(
    connector_name: str,
    connector_type: str = "sdn",
    adom: str = "root",
) -> dict[str, Any]:
    """Test connector connectivity to verify configuration.
    
    Performs connectivity test to validate:
    - Network reachability
    - Credentials and authentication
    - API endpoint availability
    - Permission levels
    
    Args:
        connector_name: Connector name
        connector_type: Connector type - "sdn", "cloud", or "fabric"
        adom: ADOM name (default: "root")
    
    Returns:
        Dictionary with test results
    
    Example:
        result = test_connector_connectivity(
            connector_name="AWS-Prod",
            connector_type="sdn",
            adom="root"
        )
    """
    try:
        api = _get_connector_api()
        test_result = await api.test_connector_connectivity(
            connector_name=connector_name,
            connector_type=connector_type,
            adom=adom,
        )
        return {
            "status": "success",
            "test_result": test_result,
        }
    except Exception as e:
        logger.error(f"Error testing connector connectivity: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def sync_connector_objects(
    connector_name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Synchronize connector objects with FortiManager.
    
    Pulls latest objects (addresses, services, routes) from the connected
    platform and updates FortiManager's dynamic object database.
    
    Args:
        connector_name: Connector name
        adom: ADOM name (default: "root")
    
    Returns:
        Dictionary with sync result
    
    Example:
        result = sync_connector_objects(
            connector_name="AWS-Prod",
            adom="root"
        )
    """
    try:
        api = _get_connector_api()
        sync_result = await api.sync_connector_objects(
            connector_name=connector_name,
            adom=adom,
        )
        return {
            "status": "success",
            "sync_result": sync_result,
        }
    except Exception as e:
        logger.error(f"Error syncing connector objects: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_connector_route_table(
    connector_name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Get route table from SDN connector.
    
    Retrieves routing information from cloud platforms used for:
    - Dynamic address object population
    - Network topology mapping
    - Route-based policy creation
    
    Args:
        connector_name: SDN connector name
        adom: ADOM name (default: "root")
    
    Returns:
        Dictionary with route table entries
    
    Example:
        result = get_connector_route_table(
            connector_name="AWS-Prod",
            adom="root"
        )
    """
    try:
        api = _get_connector_api()
        route_table = await api.get_connector_route_table(
            connector_name=connector_name,
            adom=adom,
        )
        return {
            "status": "success",
            "route_table": route_table,
        }
    except Exception as e:
        logger.error(f"Error getting connector route table: {e}")
        return {"status": "error", "message": str(e)}

