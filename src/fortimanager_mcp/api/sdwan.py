"""SD-WAN Management API client for FortiManager."""

from typing import Any

from fortimanager_mcp.api.client import FortiManagerClient


class SdwanAPI:
    """API client for SD-WAN management operations."""

    def __init__(self, client: FortiManagerClient):
        """Initialize SD-WAN API client."""
        self.client = client

    # SD-WAN Zones
    async def list_sdwan_zones(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List SD-WAN zones in an ADOM.
        
        SD-WAN zones group interfaces for load balancing and failover.
        """
        url = f"/pm/config/adom/{adom}/obj/system/sdwan/zone"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def get_sdwan_zone(
        self,
        name: str,
        adom: str = "root",
    ) -> dict[str, Any] | None:
        """Get SD-WAN zone details."""
        url = f"/pm/config/adom/{adom}/obj/system/sdwan/zone/{name}"
        return await self.client.get(url)

    async def create_sdwan_zone(
        self,
        name: str,
        adom: str = "root",
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Create an SD-WAN zone."""
        url = f"/pm/config/adom/{adom}/obj/system/sdwan/zone"
        data = {"name": name, **kwargs}
        return await self.client.add(url, data)

    async def delete_sdwan_zone(
        self,
        name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Delete an SD-WAN zone."""
        url = f"/pm/config/adom/{adom}/obj/system/sdwan/zone/{name}"
        return await self.client.delete(url)

    # SD-WAN Health Checks
    async def list_sdwan_health_checks(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List SD-WAN health check monitors.
        
        Health checks monitor link quality and availability for SD-WAN members.
        """
        url = f"/pm/config/adom/{adom}/obj/system/sdwan/health-check"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def get_sdwan_health_check(
        self,
        name: str,
        adom: str = "root",
    ) -> dict[str, Any] | None:
        """Get SD-WAN health check details."""
        url = f"/pm/config/adom/{adom}/obj/system/sdwan/health-check/{name}"
        return await self.client.get(url)

    async def create_sdwan_health_check(
        self,
        name: str,
        server: str,
        protocol: str = "ping",
        adom: str = "root",
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Create an SD-WAN health check monitor.
        
        Args:
            name: Health check name
            server: Server IP to monitor
            protocol: Protocol to use (ping, tcp-echo, udp-echo, http, dns, etc.)
            adom: ADOM name
            **kwargs: Additional health check parameters (interval, probe-timeout, etc.)
        """
        url = f"/pm/config/adom/{adom}/obj/system/sdwan/health-check"
        data = {
            "name": name,
            "server": server,
            "protocol": protocol,
            **kwargs
        }
        return await self.client.add(url, data)

    async def delete_sdwan_health_check(
        self,
        name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Delete an SD-WAN health check."""
        url = f"/pm/config/adom/{adom}/obj/system/sdwan/health-check/{name}"
        return await self.client.delete(url)

    # SD-WAN Services (Rules)
    async def list_sdwan_services(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List SD-WAN service rules.
        
        Service rules determine which path traffic should take based on various criteria.
        """
        url = f"/pm/config/adom/{adom}/obj/system/sdwan/service"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def get_sdwan_service(
        self,
        service_id: int,
        adom: str = "root",
    ) -> dict[str, Any] | None:
        """Get SD-WAN service rule details."""
        url = f"/pm/config/adom/{adom}/obj/system/sdwan/service/{service_id}"
        return await self.client.get(url)

    async def create_sdwan_service(
        self,
        name: str,
        mode: str = "auto",
        adom: str = "root",
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Create an SD-WAN service rule.
        
        Args:
            name: Service rule name
            mode: Service mode (auto, manual, priority, sla)
            adom: ADOM name
            **kwargs: Additional service parameters (dst, src, priority-members, etc.)
        """
        url = f"/pm/config/adom/{adom}/obj/system/sdwan/service"
        data = {
            "name": name,
            "mode": mode,
            **kwargs
        }
        return await self.client.add(url, data)

    async def delete_sdwan_service(
        self,
        service_id: int,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Delete an SD-WAN service rule."""
        url = f"/pm/config/adom/{adom}/obj/system/sdwan/service/{service_id}"
        return await self.client.delete(url)

    # SD-WAN Members
    async def list_sdwan_members(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List SD-WAN member interfaces.
        
        Members are the WAN interfaces participating in SD-WAN.
        """
        url = f"/pm/config/adom/{adom}/obj/system/sdwan/members"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    # Traffic Classes (Application Profiles)
    async def list_traffic_classes(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List traffic classes for SD-WAN application-based routing."""
        url = f"/pm/config/adom/{adom}/obj/firewall/traffic-class"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def get_traffic_class(
        self,
        class_id: int,
        adom: str = "root",
    ) -> dict[str, Any] | None:
        """Get traffic class details."""
        url = f"/pm/config/adom/{adom}/obj/firewall/traffic-class/{class_id}"
        return await self.client.get(url)

    async def create_traffic_class(
        self,
        class_name: str,
        adom: str = "root",
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Create a traffic class."""
        url = f"/pm/config/adom/{adom}/obj/firewall/traffic-class"
        data = {"class-name": class_name, **kwargs}
        return await self.client.add(url, data)

    async def delete_traffic_class(
        self,
        class_id: int,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Delete a traffic class."""
        url = f"/pm/config/adom/{adom}/obj/firewall/traffic-class/{class_id}"
        return await self.client.delete(url)

    # WAN Profiles (SD-WAN Templates)
    async def list_wan_profiles(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List WAN profiles (SD-WAN templates).
        
        WAN profiles are templates for SD-WAN configuration.
        """
        url = f"/pm/wanprof/adom/{adom}"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def get_wan_profile(
        self,
        name: str,
        adom: str = "root",
    ) -> dict[str, Any] | None:
        """Get WAN profile details."""
        url = f"/pm/wanprof/adom/{adom}/{name}"
        return await self.client.get(url)

