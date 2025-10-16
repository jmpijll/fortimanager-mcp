"""FortiManager Docker Management API operations."""

import logging
from typing import Any

logger = logging.getLogger(__name__)


class DockerAPI:
    """Docker container management operations.
    
    Handles Docker containers on FortiManager for extensions.
    """

    def __init__(self, client: Any) -> None:
        """Initialize DockerAPI.
        
        Args:
            client: FortiManager API client
        """
        self.client = client

    # =========================================================================
    # Phase 36: Docker Management
    # =========================================================================

    async def list_docker_containers(self) -> list[dict[str, Any]]:
        """List Docker containers running on FortiManager.
        
        FortiManager supports Docker containers for:
        - Custom integrations
        - Third-party tools
        - Extension modules
        
        Returns:
            List of Docker containers
        """
        url = "/cli/global/system/docker/container"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def get_docker_container_status(
        self,
        container_name: str,
    ) -> dict[str, Any]:
        """Get Docker container status.
        
        Retrieves status and resource usage of a specific container.
        
        Args:
            container_name: Container name
            
        Returns:
            Container status and metrics
        """
        url = f"/cli/global/system/docker/container/{container_name}/status"
        data = await self.client.get(url)
        return data if isinstance(data, dict) else {}

