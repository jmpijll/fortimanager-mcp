"""Docker Management MCP Tools."""

import logging
from typing import Any

from fortimanager_mcp.api.docker import DockerAPI
from fortimanager_mcp.server import get_fmg_client, mcp

logger = logging.getLogger(__name__)


def _get_docker_api() -> DockerAPI:
    client = get_fmg_client()
    if not client:
        raise RuntimeError("FortiManager client not initialized")
    return DockerAPI(client)


# =============================================================================
# Phase 36: Docker Management
# =============================================================================


@mcp.tool()
async def list_docker_containers() -> dict[str, Any]:
    """List Docker containers running on FortiManager.
    
    FortiManager supports Docker containers for extensibility:
    - **Custom integrations**: Connect to external systems
    - **Third-party tools**: Security scanners, SIEM connectors
    - **Extension modules**: Custom automation and reporting
    
    Container use cases:
    - API gateways for external integrations
    - Data transformation and enrichment
    - Custom analytics and dashboards
    - Automation workflow engines
    
    Returns:
        Dictionary with list of Docker containers
    
    Example:
        result = list_docker_containers()
        # Returns all running containers with names and status
    """
    try:
        api = _get_docker_api()
        containers = await api.list_docker_containers()
        return {
            "status": "success",
            "count": len(containers),
            "containers": containers,
        }
    except Exception as e:
        logger.error(f"Error listing Docker containers: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_docker_container_status(container_name: str) -> dict[str, Any]:
    """Get Docker container status and resource usage.
    
    Retrieves detailed status and metrics for a specific container:
    - **Running state**: Up, down, restarting
    - **Resource usage**: CPU, memory, network
    - **Health status**: Healthy, unhealthy, starting
    - **Uptime**: How long container has been running
    
    Use this to:
    - Monitor container health
    - Troubleshoot integration issues
    - Track resource consumption
    - Verify container operations
    
    Args:
        container_name: Name of the Docker container
    
    Returns:
        Dictionary with container status and metrics
    
    Example:
        result = get_docker_container_status(
            container_name="api-gateway"
        )
    """
    try:
        api = _get_docker_api()
        status = await api.get_docker_container_status(
            container_name=container_name,
        )
        return {
            "status": "success",
            "container": container_name,
            "container_status": status,
        }
    except Exception as e:
        logger.error(f"Error getting Docker container status: {e}")
        return {"status": "error", "message": str(e)}


