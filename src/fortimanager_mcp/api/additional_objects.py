"""Additional firewall and security objects API client."""

from typing import Any

from fortimanager_mcp.api.client import FortiManagerClient


class AdditionalObjectsAPI:
    """API client for additional firewall and security objects."""

    def __init__(self, client: FortiManagerClient):
        """Initialize Additional Objects API client."""
        self.client = client

    # ============================================================================
    # Internet Service Objects
    # ============================================================================

    async def list_internet_service_names(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List internet service name objects.
        
        Internet services are predefined FortiGuard service objects
        for popular applications and services.
        
        Args:
            adom: ADOM name
            
        Returns:
            List of internet service name objects
        """
        url = f"/pm/config/adom/{adom}/obj/firewall/internet-service-name"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def get_internet_service_name(
        self,
        name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get internet service name details.
        
        Args:
            name: Internet service name
            adom: ADOM name
            
        Returns:
            Internet service name object
        """
        url = f"/pm/config/adom/{adom}/obj/firewall/internet-service-name/{name}"
        return await self.client.get(url)

    async def list_internet_service_groups(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List internet service group objects.
        
        Groups of internet services for use in firewall policies.
        
        Args:
            adom: ADOM name
            
        Returns:
            List of internet service group objects
        """
        url = f"/pm/config/adom/{adom}/obj/firewall/internet-service-group"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def create_internet_service_group(
        self,
        name: str,
        members: list[str],
        adom: str = "root",
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Create an internet service group.
        
        Args:
            name: Group name
            members: List of internet service names
            adom: ADOM name
            **kwargs: Additional parameters
            
        Returns:
            Created group object
        """
        data = {
            "name": name,
            "member": members,
            **kwargs,
        }
        url = f"/pm/config/adom/{adom}/obj/firewall/internet-service-group"
        return await self.client.add(url, data=data)

    async def delete_internet_service_group(
        self,
        name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Delete an internet service group.
        
        Args:
            name: Group name
            adom: ADOM name
            
        Returns:
            Deletion result
        """
        url = f"/pm/config/adom/{adom}/obj/firewall/internet-service-group/{name}"
        return await self.client.delete(url)

    # ============================================================================
    # Security Profile Groups
    # ============================================================================

    async def list_profile_groups(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List security profile groups.
        
        Profile groups bundle multiple security profiles (AV, Web Filter,
        IPS, etc.) for easy application to firewall policies.
        
        Args:
            adom: ADOM name
            
        Returns:
            List of profile group objects
        """
        url = f"/pm/config/adom/{adom}/obj/firewall/profile-group"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def get_profile_group(
        self,
        name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get profile group details.
        
        Args:
            name: Profile group name
            adom: ADOM name
            
        Returns:
            Profile group object
        """
        url = f"/pm/config/adom/{adom}/obj/firewall/profile-group/{name}"
        return await self.client.get(url)

    async def create_profile_group(
        self,
        name: str,
        adom: str = "root",
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Create a security profile group.
        
        Args:
            name: Profile group name
            adom: ADOM name
            **kwargs: Profile assignments (av-profile, webfilter-profile,
                     ips-sensor, application-list, dnsfilter-profile, etc.)
            
        Returns:
            Created profile group
            
        Example:
            create_profile_group(
                name="full-security",
                av_profile="default",
                webfilter_profile="default",
                ips_sensor="default",
                application_list="default"
            )
        """
        data = {"name": name, **kwargs}
        url = f"/pm/config/adom/{adom}/obj/firewall/profile-group"
        return await self.client.add(url, data=data)

    async def update_profile_group(
        self,
        name: str,
        adom: str = "root",
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Update a security profile group.
        
        Args:
            name: Profile group name
            adom: ADOM name
            **kwargs: Profile assignments to update
            
        Returns:
            Updated profile group
        """
        url = f"/pm/config/adom/{adom}/obj/firewall/profile-group/{name}"
        return await self.client.update(url, data=kwargs)

    async def delete_profile_group(
        self,
        name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Delete a security profile group.
        
        Args:
            name: Profile group name
            adom: ADOM name
            
        Returns:
            Deletion result
        """
        url = f"/pm/config/adom/{adom}/obj/firewall/profile-group/{name}"
        return await self.client.delete(url)

    # ============================================================================
    # Custom Applications
    # ============================================================================

    async def list_custom_applications(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List custom application signatures.
        
        Custom applications extend FortiGuard's application control
        with user-defined application signatures.
        
        Args:
            adom: ADOM name
            
        Returns:
            List of custom application objects
        """
        url = f"/pm/config/adom/{adom}/obj/application/custom"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def get_custom_application(
        self,
        tag: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get custom application details.
        
        Args:
            tag: Application tag/name
            adom: ADOM name
            
        Returns:
            Custom application object
        """
        url = f"/pm/config/adom/{adom}/obj/application/custom/{tag}"
        return await self.client.get(url)

    async def create_custom_application(
        self,
        tag: str,
        protocol: str,
        adom: str = "root",
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Create a custom application signature.
        
        Args:
            tag: Application tag/name
            protocol: Protocol (TCP/UDP, TCP, UDP)
            adom: ADOM name
            **kwargs: Additional parameters (signature, port-ranges, etc.)
            
        Returns:
            Created custom application
        """
        data = {
            "tag": tag,
            "protocol": protocol,
            **kwargs,
        }
        url = f"/pm/config/adom/{adom}/obj/application/custom"
        return await self.client.add(url, data=data)

    async def delete_custom_application(
        self,
        tag: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Delete a custom application.
        
        Args:
            tag: Application tag/name
            adom: ADOM name
            
        Returns:
            Deletion result
        """
        url = f"/pm/config/adom/{adom}/obj/application/custom/{tag}"
        return await self.client.delete(url)

    # ============================================================================
    # DNS Filter Domains
    # ============================================================================

    async def list_dns_filter_domains(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List DNS filter domain lists.
        
        DNS filter domains are custom domain blocklists/allowlists
        for DNS filtering policies.
        
        Args:
            adom: ADOM name
            
        Returns:
            List of DNS filter domain objects
        """
        url = f"/pm/config/adom/{adom}/obj/dnsfilter/domain-filter"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def get_dns_filter_domain(
        self,
        id: int,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get DNS filter domain details.
        
        Args:
            id: Domain filter ID
            adom: ADOM name
            
        Returns:
            DNS filter domain object
        """
        url = f"/pm/config/adom/{adom}/obj/dnsfilter/domain-filter/{id}"
        return await self.client.get(url)

    async def create_dns_filter_domain(
        self,
        name: str,
        adom: str = "root",
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Create a DNS filter domain list.
        
        Args:
            name: Domain filter name
            adom: ADOM name
            **kwargs: Additional parameters (entries with domain/action)
            
        Returns:
            Created DNS filter domain
            
        Example:
            create_dns_filter_domain(
                name="blocked-domains",
                entries=[
                    {"domain": "*.malware.com", "action": "block"},
                    {"domain": "phishing.example", "action": "block"}
                ]
            )
        """
        data = {"name": name, **kwargs}
        url = f"/pm/config/adom/{adom}/obj/dnsfilter/domain-filter"
        return await self.client.add(url, data=data)

    async def delete_dns_filter_domain(
        self,
        id: int,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Delete a DNS filter domain list.
        
        Args:
            id: Domain filter ID
            adom: ADOM name
            
        Returns:
            Deletion result
        """
        url = f"/pm/config/adom/{adom}/obj/dnsfilter/domain-filter/{id}"
        return await self.client.delete(url)

