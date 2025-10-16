"""System proxy JSON operations API module."""

from typing import Any

from fortimanager_mcp.api.client import FortiManagerClient


class SysProxyAPI:
    """System proxy JSON operations for device communication."""

    def __init__(self, client: FortiManagerClient) -> None:
        """Initialize Sys Proxy API.

        Args:
            client: FortiManager client instance
        """
        self.client = client

    async def execute_proxy_json(
        self,
        device_name: str,
        commands: list[str],
        adom: str = "root",
    ) -> dict[str, Any]:
        """Execute JSON commands on a device via system proxy.

        Allows execution of FortiGate JSON-RPC commands through FortiManager.

        Args:
            device_name: Target device name
            commands: List of JSON-RPC commands
            adom: ADOM name

        Returns:
            Command execution results
        """
        data = {
            "adom": adom,
            "device": device_name,
            "commands": commands,
        }
        return await self.client.exec("/sys/proxy/json", data=data)

    async def get_proxy_capabilities(
        self,
        device_name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get proxy capabilities and supported operations for a device.

        Args:
            device_name: Target device name
            adom: ADOM name

        Returns:
            Proxy capabilities
        """
        url = f"/dvmdb/adom/{adom}/device/{device_name}/proxy/capabilities"
        return await self.client.get(url)


