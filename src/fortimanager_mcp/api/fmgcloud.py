"""FortiManager Cloud Integration API operations."""

import logging
from typing import Any

logger = logging.getLogger(__name__)


class FMGCloudAPI:
    """FortiManager Cloud integration operations.
    
    Handles cloud-based FortiManager services and integrations.
    """

    def __init__(self, client: Any) -> None:
        """Initialize FMGCloudAPI.
        
        Args:
            client: FortiManager API client
        """
        self.client = client

    # =========================================================================
    # Phase 35: FMG Cloud Operations
    # =========================================================================

    async def get_cloud_service_status(self) -> dict[str, Any]:
        """Get FortiManager cloud service status.
        
        Retrieves status of cloud-based FortiManager services including:
        - Cloud connectivity
        - Service availability
        - Subscription status
        
        Returns:
            Cloud service status
        """
        url = "/sys/cloud/status"
        data = await self.client.get(url)
        return data if isinstance(data, dict) else {}

    async def get_cloud_account_info(self) -> dict[str, Any]:
        """Get cloud account information.
        
        Retrieves FortiCloud account details and subscription info.
        
        Returns:
            Cloud account information
        """
        url = "/sys/cloud/account"
        data = await self.client.get(url)
        return data if isinstance(data, dict) else {}

    async def sync_with_cloud(self) -> dict[str, Any]:
        """Synchronize FortiManager with FortiCloud.
        
        Triggers synchronization of configurations and data
        with FortiCloud services.
        
        Returns:
            Sync operation result
        """
        url = "/sys/cloud/sync"
        return await self.client.exec(url, data={})

