"""FortiManager Cyber Security Fabric (CSF) API operations."""

import logging
from typing import Any

logger = logging.getLogger(__name__)


class CSFAPI:
    """Cyber Security Fabric operations.
    
    Handles Security Fabric topology and fabric devices.
    """

    def __init__(self, client: Any) -> None:
        """Initialize CSFAPI.
        
        Args:
            client: FortiManager API client
        """
        self.client = client

    # =========================================================================
    # Phase 33: CSF (Cyber Security Fabric)
    # =========================================================================

    async def get_fabric_topology(
        self,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get Security Fabric topology.
        
        Retrieves the fabric topology showing all connected devices
        and their relationships in the Security Fabric.
        
        Args:
            adom: ADOM name
            
        Returns:
            Fabric topology information
        """
        url = f"/dvmdb/adom/{adom}/fabric/topology"
        data = await self.client.get(url)
        return data if isinstance(data, dict) else {}

    async def list_fabric_devices(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List devices in the Security Fabric.
        
        Shows all FortiGate devices participating in the Security Fabric
        including root and downstream FortiGates.
        
        Args:
            adom: ADOM name
            
        Returns:
            List of fabric devices
        """
        url = f"/dvmdb/adom/{adom}/fabric/devices"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def get_fabric_authorization_status(
        self,
        device_name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get fabric authorization status for a device.
        
        Shows whether a device is authorized to join the Security Fabric.
        
        Args:
            device_name: Device name
            adom: ADOM name
            
        Returns:
            Authorization status
        """
        url = f"/dvmdb/adom/{adom}/fabric/authorization/{device_name}"
        data = await self.client.get(url)
        return data if isinstance(data, dict) else {}

