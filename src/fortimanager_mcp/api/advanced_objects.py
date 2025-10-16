"""Advanced firewall objects API client for FortiManager."""

from typing import Any

from fortimanager_mcp.api.client import FortiManagerClient


class AdvancedObjectsAPI:
    """API client for advanced firewall objects (VIPs, IP pools, schedules, etc.)."""

    def __init__(self, client: FortiManagerClient):
        """Initialize Advanced Objects API client."""
        self.client = client

    # ============================================================================
    # Virtual IPs (VIPs)
    # ============================================================================

    async def list_vips(self, adom: str = "root") -> list[dict[str, Any]]:
        """List all virtual IPs (VIPs).
        
        VIPs are used for destination NAT and port forwarding.
        
        Args:
            adom: ADOM name
            
        Returns:
            List of VIP objects
        """
        url = f"/pm/config/adom/{adom}/obj/firewall/vip"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def get_vip(self, name: str, adom: str = "root") -> dict[str, Any]:
        """Get virtual IP details.
        
        Args:
            name: VIP name
            adom: ADOM name
            
        Returns:
            VIP object details
        """
        url = f"/pm/config/adom/{adom}/obj/firewall/vip/{name}"
        return await self.client.get(url)

    async def create_vip(
        self,
        name: str,
        extip: str,
        mappedip: str,
        adom: str = "root",
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Create a virtual IP.
        
        Args:
            name: VIP name
            extip: External IP address or range
            mappedip: Mapped internal IP address or range
            adom: ADOM name
            **kwargs: Additional VIP parameters (extintf, portforward, protocol, etc.)
            
        Returns:
            Created VIP object
            
        Example:
            # Port forwarding
            create_vip(
                name="web-server-vip",
                extip="203.0.113.10",
                mappedip="192.168.1.10",
                extintf=["wan1"],
                portforward="enable",
                protocol="tcp",
                extport="443",
                mappedport="8443"
            )
        """
        data = {
            "name": name,
            "extip": [extip] if isinstance(extip, str) else extip,
            "mappedip": [mappedip] if isinstance(mappedip, str) else mappedip,
            **kwargs,
        }
        url = f"/pm/config/adom/{adom}/obj/firewall/vip"
        return await self.client.add(url, data=data)

    async def update_vip(
        self,
        name: str,
        adom: str = "root",
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Update a virtual IP.
        
        Args:
            name: VIP name
            adom: ADOM name
            **kwargs: VIP parameters to update
            
        Returns:
            Updated VIP object
        """
        url = f"/pm/config/adom/{adom}/obj/firewall/vip/{name}"
        return await self.client.update(url, data=kwargs)

    async def delete_vip(self, name: str, adom: str = "root") -> dict[str, Any]:
        """Delete a virtual IP.
        
        Args:
            name: VIP name
            adom: ADOM name
            
        Returns:
            Deletion result
        """
        url = f"/pm/config/adom/{adom}/obj/firewall/vip/{name}"
        return await self.client.delete(url)

    # ============================================================================
    # VIP Groups
    # ============================================================================

    async def list_vip_groups(self, adom: str = "root") -> list[dict[str, Any]]:
        """List all VIP groups.
        
        Args:
            adom: ADOM name
            
        Returns:
            List of VIP group objects
        """
        url = f"/pm/config/adom/{adom}/obj/firewall/vipgrp"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def get_vip_group(self, name: str, adom: str = "root") -> dict[str, Any]:
        """Get VIP group details.
        
        Args:
            name: VIP group name
            adom: ADOM name
            
        Returns:
            VIP group object
        """
        url = f"/pm/config/adom/{adom}/obj/firewall/vipgrp/{name}"
        return await self.client.get(url)

    async def create_vip_group(
        self,
        name: str,
        members: list[str],
        adom: str = "root",
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Create a VIP group.
        
        Args:
            name: VIP group name
            members: List of VIP names to include
            adom: ADOM name
            **kwargs: Additional parameters
            
        Returns:
            Created VIP group object
        """
        data = {
            "name": name,
            "member": members,
            **kwargs,
        }
        url = f"/pm/config/adom/{adom}/obj/firewall/vipgrp"
        return await self.client.add(url, data=data)

    async def update_vip_group(
        self,
        name: str,
        adom: str = "root",
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Update a VIP group.
        
        Args:
            name: VIP group name
            adom: ADOM name
            **kwargs: Parameters to update
            
        Returns:
            Updated VIP group object
        """
        url = f"/pm/config/adom/{adom}/obj/firewall/vipgrp/{name}"
        return await self.client.update(url, data=kwargs)

    async def delete_vip_group(self, name: str, adom: str = "root") -> dict[str, Any]:
        """Delete a VIP group.
        
        Args:
            name: VIP group name
            adom: ADOM name
            
        Returns:
            Deletion result
        """
        url = f"/pm/config/adom/{adom}/obj/firewall/vipgrp/{name}"
        return await self.client.delete(url)

    # ============================================================================
    # IP Pools
    # ============================================================================

    async def list_ip_pools(self, adom: str = "root") -> list[dict[str, Any]]:
        """List all IP pools.
        
        IP pools are used for source NAT (SNAT).
        
        Args:
            adom: ADOM name
            
        Returns:
            List of IP pool objects
        """
        url = f"/pm/config/adom/{adom}/obj/firewall/ippool"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def get_ip_pool(self, name: str, adom: str = "root") -> dict[str, Any]:
        """Get IP pool details.
        
        Args:
            name: IP pool name
            adom: ADOM name
            
        Returns:
            IP pool object
        """
        url = f"/pm/config/adom/{adom}/obj/firewall/ippool/{name}"
        return await self.client.get(url)

    async def create_ip_pool(
        self,
        name: str,
        startip: str,
        endip: str,
        adom: str = "root",
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Create an IP pool for source NAT.
        
        Args:
            name: IP pool name
            startip: Starting IP address
            endip: Ending IP address
            adom: ADOM name
            **kwargs: Additional parameters (type, arp-reply, etc.)
            
        Returns:
            Created IP pool object
            
        Example:
            create_ip_pool(
                name="internet-nat-pool",
                startip="203.0.113.100",
                endip="203.0.113.199",
                type="overload"
            )
        """
        data = {
            "name": name,
            "startip": startip,
            "endip": endip,
            **kwargs,
        }
        url = f"/pm/config/adom/{adom}/obj/firewall/ippool"
        return await self.client.add(url, data=data)

    async def update_ip_pool(
        self,
        name: str,
        adom: str = "root",
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Update an IP pool.
        
        Args:
            name: IP pool name
            adom: ADOM name
            **kwargs: Parameters to update
            
        Returns:
            Updated IP pool object
        """
        url = f"/pm/config/adom/{adom}/obj/firewall/ippool/{name}"
        return await self.client.update(url, data=kwargs)

    async def delete_ip_pool(self, name: str, adom: str = "root") -> dict[str, Any]:
        """Delete an IP pool.
        
        Args:
            name: IP pool name
            adom: ADOM name
            
        Returns:
            Deletion result
        """
        url = f"/pm/config/adom/{adom}/obj/firewall/ippool/{name}"
        return await self.client.delete(url)

    # ============================================================================
    # Schedules
    # ============================================================================

    async def list_schedules_onetime(self, adom: str = "root") -> list[dict[str, Any]]:
        """List all one-time schedules.
        
        Args:
            adom: ADOM name
            
        Returns:
            List of one-time schedule objects
        """
        url = f"/pm/config/adom/{adom}/obj/firewall/schedule/onetime"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def list_schedules_recurring(self, adom: str = "root") -> list[dict[str, Any]]:
        """List all recurring schedules.
        
        Args:
            adom: ADOM name
            
        Returns:
            List of recurring schedule objects
        """
        url = f"/pm/config/adom/{adom}/obj/firewall/schedule/recurring"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def list_schedules_group(self, adom: str = "root") -> list[dict[str, Any]]:
        """List all schedule groups.
        
        Args:
            adom: ADOM name
            
        Returns:
            List of schedule group objects
        """
        url = f"/pm/config/adom/{adom}/obj/firewall/schedule/group"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def create_schedule_recurring(
        self,
        name: str,
        day: list[str],
        start: str,
        end: str,
        adom: str = "root",
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Create a recurring schedule.
        
        Args:
            name: Schedule name
            day: List of days (sunday, monday, tuesday, etc.)
            start: Start time (HH:MM format)
            end: End time (HH:MM format)
            adom: ADOM name
            **kwargs: Additional parameters
            
        Returns:
            Created schedule object
            
        Example:
            create_schedule_recurring(
                name="business-hours",
                day=["monday", "tuesday", "wednesday", "thursday", "friday"],
                start="08:00",
                end="18:00"
            )
        """
        data = {
            "name": name,
            "day": day,
            "start": start,
            "end": end,
            **kwargs,
        }
        url = f"/pm/config/adom/{adom}/obj/firewall/schedule/recurring"
        return await self.client.add(url, data=data)

    async def create_schedule_onetime(
        self,
        name: str,
        start: str,
        end: str,
        adom: str = "root",
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Create a one-time schedule.
        
        Args:
            name: Schedule name
            start: Start date/time (YYYY-MM-DD HH:MM format)
            end: End date/time (YYYY-MM-DD HH:MM format)
            adom: ADOM name
            **kwargs: Additional parameters
            
        Returns:
            Created schedule object
        """
        data = {
            "name": name,
            "start": start,
            "end": end,
            **kwargs,
        }
        url = f"/pm/config/adom/{adom}/obj/firewall/schedule/onetime"
        return await self.client.add(url, data=data)

    async def delete_schedule_recurring(
        self,
        name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Delete a recurring schedule.
        
        Args:
            name: Schedule name
            adom: ADOM name
            
        Returns:
            Deletion result
        """
        url = f"/pm/config/adom/{adom}/obj/firewall/schedule/recurring/{name}"
        return await self.client.delete(url)

    async def delete_schedule_onetime(
        self,
        name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Delete a one-time schedule.
        
        Args:
            name: Schedule name
            adom: ADOM name
            
        Returns:
            Deletion result
        """
        url = f"/pm/config/adom/{adom}/obj/firewall/schedule/onetime/{name}"
        return await self.client.delete(url)

    # ============================================================================
    # Wildcard FQDN
    # ============================================================================

    async def list_wildcard_fqdns(self, adom: str = "root") -> list[dict[str, Any]]:
        """List all wildcard FQDNs.
        
        Wildcard FQDNs allow pattern-based domain matching (e.g., *.example.com).
        
        Args:
            adom: ADOM name
            
        Returns:
            List of wildcard FQDN objects
        """
        url = f"/pm/config/adom/{adom}/obj/firewall/wildcard-fqdn/custom"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def get_wildcard_fqdn(self, name: str, adom: str = "root") -> dict[str, Any]:
        """Get wildcard FQDN details.
        
        Args:
            name: Wildcard FQDN name
            adom: ADOM name
            
        Returns:
            Wildcard FQDN object
        """
        url = f"/pm/config/adom/{adom}/obj/firewall/wildcard-fqdn/custom/{name}"
        return await self.client.get(url)

    async def create_wildcard_fqdn(
        self,
        name: str,
        wildcard_fqdn: str,
        adom: str = "root",
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Create a wildcard FQDN.
        
        Args:
            name: Object name
            wildcard_fqdn: Wildcard domain pattern (e.g., *.example.com)
            adom: ADOM name
            **kwargs: Additional parameters
            
        Returns:
            Created wildcard FQDN object
            
        Example:
            create_wildcard_fqdn(
                name="all-google-domains",
                wildcard_fqdn="*.google.com"
            )
        """
        data = {
            "name": name,
            "wildcard-fqdn": wildcard_fqdn,
            **kwargs,
        }
        url = f"/pm/config/adom/{adom}/obj/firewall/wildcard-fqdn/custom"
        return await self.client.add(url, data=data)

    async def delete_wildcard_fqdn(
        self,
        name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Delete a wildcard FQDN.
        
        Args:
            name: Wildcard FQDN name
            adom: ADOM name
            
        Returns:
            Deletion result
        """
        url = f"/pm/config/adom/{adom}/obj/firewall/wildcard-fqdn/custom/{name}"
        return await self.client.delete(url)

