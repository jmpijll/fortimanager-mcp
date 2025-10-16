"""QoS management operations API module."""

from typing import Any

from fortimanager_mcp.api.client import FortiManagerClient


class QoSAPI:
    """Quality of Service management operations."""

    def __init__(self, client: FortiManagerClient) -> None:
        """Initialize QoS API.

        Args:
            client: FortiManager client instance
        """
        self.client = client

    async def list_qos_policies(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List QoS policies.

        Args:
            adom: ADOM name

        Returns:
            List of QoS policies
        """
        url = f"/pm/config/adom/{adom}/obj/firewall/shaping-policy"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def get_qos_statistics(
        self,
        device_name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get QoS statistics for a device.

        Args:
            device_name: Device name
            adom: ADOM name

        Returns:
            QoS statistics
        """
        url = f"/monitor/adom/{adom}/device/{device_name}/qos/stats"
        return await self.client.get(url)


