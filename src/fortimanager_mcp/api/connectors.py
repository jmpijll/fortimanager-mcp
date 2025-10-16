"""FortiManager Connector Management API operations."""

import logging
from typing import Any

logger = logging.getLogger(__name__)


class ConnectorAPI:
    """Connector management operations.
    
    Handles SDN connectors, cloud connectors, and Fabric connectors.
    """

    def __init__(self, client: Any) -> None:
        """Initialize ConnectorAPI.
        
        Args:
            client: FortiManager API client
        """
        self.client = client

    # =========================================================================
    # Phase 31: SDN Connectors
    # =========================================================================

    async def list_sdn_connectors(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List SDN (Software-Defined Networking) connectors.
        
        SDN connectors integrate with cloud and virtualization platforms:
        - AWS, Azure, GCP
        - VMware NSX, vCenter
        - OpenStack, Kubernetes
        - ACI, Nuage
        
        Args:
            adom: ADOM name
            
        Returns:
            List of SDN connectors
        """
        url = f"/pm/config/adom/{adom}/obj/system/sdn-connector"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def get_sdn_connector(
        self,
        name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get SDN connector details.
        
        Args:
            name: Connector name
            adom: ADOM name
            
        Returns:
            SDN connector configuration
        """
        url = f"/pm/config/adom/{adom}/obj/system/sdn-connector/{name}"
        data = await self.client.get(url)
        return data if isinstance(data, dict) else {}

    async def refresh_sdn_connector(
        self,
        name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Refresh SDN connector to sync with cloud platform.
        
        Args:
            name: Connector name
            adom: ADOM name
            
        Returns:
            Refresh result
        """
        url = f"/pm/config/adom/{adom}/obj/system/sdn-connector/{name}/refresh"
        return await self.client.exec(url, data={})

    async def get_sdn_connector_status(
        self,
        name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get SDN connector connection status.
        
        Args:
            name: Connector name
            adom: ADOM name
            
        Returns:
            Connector status including connectivity and last update
        """
        url = f"/pm/config/adom/{adom}/obj/system/sdn-connector/{name}/status"
        data = await self.client.get(url)
        return data if isinstance(data, dict) else {}

    # =========================================================================
    # Phase 31: Cloud Connectors
    # =========================================================================

    async def list_cloud_connectors(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List cloud platform connectors.
        
        Cloud connectors provide integration with cloud security services.
        
        Args:
            adom: ADOM name
            
        Returns:
            List of cloud connectors
        """
        url = f"/pm/config/adom/{adom}/obj/system/cloud-connector"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def get_cloud_connector_services(
        self,
        connector_name: str,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """Get cloud services available through a connector.
        
        Args:
            connector_name: Cloud connector name
            adom: ADOM name
            
        Returns:
            List of available cloud services
        """
        url = f"/pm/config/adom/{adom}/obj/system/cloud-connector/{connector_name}/services"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    # =========================================================================
    # Phase 31: Fabric Connectors
    # =========================================================================

    async def list_fabric_connectors(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List Security Fabric connectors.
        
        Fabric connectors integrate with Fortinet Security Fabric ecosystem:
        - FortiAnalyzer
        - FortiSandbox
        - FortiWeb
        - Third-party security tools
        
        Args:
            adom: ADOM name
            
        Returns:
            List of Fabric connectors
        """
        url = f"/pm/config/adom/{adom}/obj/system/fabric-connector"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def get_fabric_connector_devices(
        self,
        connector_name: str,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """Get devices discovered through a Fabric connector.
        
        Args:
            connector_name: Fabric connector name
            adom: ADOM name
            
        Returns:
            List of discovered devices
        """
        url = f"/pm/config/adom/{adom}/obj/system/fabric-connector/{connector_name}/devices"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    # =========================================================================
    # Phase 31: Connector Operations
    # =========================================================================

    async def test_connector_connectivity(
        self,
        connector_name: str,
        connector_type: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Test connector connectivity.
        
        Args:
            connector_name: Connector name
            connector_type: Connector type (sdn, cloud, fabric)
            adom: ADOM name
            
        Returns:
            Connectivity test result
        """
        url = f"/pm/config/adom/{adom}/obj/system/{connector_type}-connector/{connector_name}/test"
        return await self.client.exec(url, data={})

    async def sync_connector_objects(
        self,
        connector_name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Synchronize connector objects with FortiManager.
        
        Pulls latest objects (addresses, services) from the connected platform.
        
        Args:
            connector_name: Connector name
            adom: ADOM name
            
        Returns:
            Sync result
        """
        url = f"/pm/config/adom/{adom}/obj/system/sdn-connector/{connector_name}/sync"
        return await self.client.exec(url, data={})

    async def get_connector_route_table(
        self,
        connector_name: str,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """Get route table from SDN connector.
        
        Retrieves routing information from cloud platforms for dynamic
        address object population.
        
        Args:
            connector_name: SDN connector name
            adom: ADOM name
            
        Returns:
            Route table entries
        """
        url = f"/pm/config/adom/{adom}/obj/system/sdn-connector/{connector_name}/route-table"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

