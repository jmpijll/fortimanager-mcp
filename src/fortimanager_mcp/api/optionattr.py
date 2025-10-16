"""Option attribute operations API module."""

from typing import Any

from fortimanager_mcp.api.client import FortiManagerClient


class OptionAttributeAPI:
    """Option attribute operations for advanced object handling."""

    def __init__(self, client: FortiManagerClient) -> None:
        """Initialize Option Attribute API.

        Args:
            client: FortiManager client instance
        """
        self.client = client

    async def get_option_attributes(
        self,
        object_type: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get available option attributes for an object type.

        Retrieves metadata about configurable options and their valid values
        for a specific object type (e.g., firewall policies, addresses).

        Args:
            object_type: Object type (e.g., "firewall.policy", "firewall.address")
            adom: ADOM name

        Returns:
            Available option attributes and their definitions
        """
        url = f"/pm/config/adom/{adom}/_data/option/{object_type}"
        return await self.client.get(url)

