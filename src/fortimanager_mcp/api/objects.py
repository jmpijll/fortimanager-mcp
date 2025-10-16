"""Firewall object management API module."""

from typing import Any

from fortimanager_mcp.api.client import FortiManagerClient
from fortimanager_mcp.api.models import FirewallAddress, FirewallAddressGroup, FirewallService


class ObjectAPI:
    """Firewall object management operations."""

    def __init__(self, client: FortiManagerClient) -> None:
        """Initialize object API.

        Args:
            client: FortiManager client instance
        """
        self.client = client

    # Firewall Address Operations
    async def list_addresses(
        self,
        adom: str = "root",
        fields: list[str] | None = None,
        filter: list[Any] | None = None,
    ) -> list[FirewallAddress]:
        """List firewall address objects.

        Args:
            adom: ADOM name
            fields: Specific fields to return
            filter: Filter criteria

        Returns:
            List of firewall addresses
        """
        url = f"/pm/config/adom/{adom}/obj/firewall/address"
        data = await self.client.get(url, fields=fields, filter=filter)
        if not isinstance(data, list):
            data = [data] if data else []

        return [FirewallAddress(**item) for item in data]

    async def get_address(self, name: str, adom: str = "root") -> FirewallAddress:
        """Get specific firewall address.

        Args:
            name: Address name
            adom: ADOM name

        Returns:
            Firewall address details
        """
        url = f"/pm/config/adom/{adom}/obj/firewall/address/{name}"
        data = await self.client.get(url)
        return FirewallAddress(**data)

    async def create_address(
        self,
        name: str,
        subnet: str,
        adom: str = "root",
        comment: str | None = None,
        **kwargs: Any,
    ) -> FirewallAddress:
        """Create firewall address object.

        Args:
            name: Address name
            subnet: IP subnet in CIDR format (e.g., 192.168.1.0/24)
            adom: ADOM name
            comment: Optional comment
            **kwargs: Additional address parameters

        Returns:
            Created firewall address
        """
        # Parse CIDR to [ip, netmask] format
        if "/" in subnet:
            ip, cidr = subnet.split("/")
            cidr_int = int(cidr)
            netmask = ".".join(
                str((0xFFFFFFFF << (32 - cidr_int) >> i) & 0xFF) for i in [24, 16, 8, 0]
            )
            subnet_list = [ip, netmask]
        else:
            subnet_list = subnet

        data = {
            "name": name,
            "type": "ipmask",
            "subnet": subnet_list,
            **kwargs,
        }

        if comment:
            data["comment"] = comment

        url = f"/pm/config/adom/{adom}/obj/firewall/address"
        await self.client.add(url, data=data)
        return await self.get_address(name, adom=adom)

    async def update_address(
        self,
        name: str,
        adom: str = "root",
        **kwargs: Any,
    ) -> FirewallAddress:
        """Update firewall address object.

        Args:
            name: Address name
            adom: ADOM name
            **kwargs: Fields to update

        Returns:
            Updated firewall address
        """
        url = f"/pm/config/adom/{adom}/obj/firewall/address/{name}"
        await self.client.set(url, data=kwargs)
        return await self.get_address(name, adom=adom)

    async def delete_address(self, name: str, adom: str = "root") -> None:
        """Delete firewall address object.

        Args:
            name: Address name
            adom: ADOM name
        """
        url = f"/pm/config/adom/{adom}/obj/firewall/address/{name}"
        await self.client.delete(url)

    # Firewall Address Group Operations
    async def list_address_groups(
        self,
        adom: str = "root",
        fields: list[str] | None = None,
        filter: list[Any] | None = None,
    ) -> list[FirewallAddressGroup]:
        """List firewall address groups.

        Args:
            adom: ADOM name
            fields: Specific fields to return
            filter: Filter criteria

        Returns:
            List of address groups
        """
        url = f"/pm/config/adom/{adom}/obj/firewall/addrgrp"
        data = await self.client.get(url, fields=fields, filter=filter)
        if not isinstance(data, list):
            data = [data] if data else []

        return [FirewallAddressGroup(**item) for item in data]

    async def create_address_group(
        self,
        name: str,
        members: list[str],
        adom: str = "root",
        comment: str | None = None,
        **kwargs: Any,
    ) -> FirewallAddressGroup:
        """Create firewall address group.

        Args:
            name: Group name
            members: List of member address names
            adom: ADOM name
            comment: Optional comment
            **kwargs: Additional group parameters

        Returns:
            Created address group
        """
        data = {
            "name": name,
            "member": members,
            **kwargs,
        }

        if comment:
            data["comment"] = comment

        url = f"/pm/config/adom/{adom}/obj/firewall/addrgrp"
        await self.client.add(url, data=data)
        return await self.get_address_group(name, adom=adom)

    async def get_address_group(self, name: str, adom: str = "root") -> FirewallAddressGroup:
        """Get specific address group.

        Args:
            name: Group name
            adom: ADOM name

        Returns:
            Address group details
        """
        url = f"/pm/config/adom/{adom}/obj/firewall/addrgrp/{name}"
        data = await self.client.get(url)
        return FirewallAddressGroup(**data)

    async def delete_address_group(self, name: str, adom: str = "root") -> None:
        """Delete firewall address group.

        Args:
            name: Group name
            adom: ADOM name
        """
        url = f"/pm/config/adom/{adom}/obj/firewall/addrgrp/{name}"
        await self.client.delete(url)

    # Firewall Service Operations
    async def list_services(
        self,
        adom: str = "root",
        fields: list[str] | None = None,
        filter: list[Any] | None = None,
    ) -> list[FirewallService]:
        """List firewall service objects.

        Args:
            adom: ADOM name
            fields: Specific fields to return
            filter: Filter criteria

        Returns:
            List of services
        """
        url = f"/pm/config/adom/{adom}/obj/firewall/service/custom"
        data = await self.client.get(url, fields=fields, filter=filter)
        if not isinstance(data, list):
            data = [data] if data else []

        return [FirewallService(**item) for item in data]

    async def create_service(
        self,
        name: str,
        protocol: str,
        port_range: str,
        adom: str = "root",
        comment: str | None = None,
        **kwargs: Any,
    ) -> FirewallService:
        """Create firewall service object.

        Args:
            name: Service name
            protocol: Protocol (TCP/UDP/ICMP)
            port_range: Port range (e.g., "80", "8000-8080")
            adom: ADOM name
            comment: Optional comment
            **kwargs: Additional service parameters

        Returns:
            Created service
        """
        data = {
            "name": name,
            "protocol": protocol.upper(),
            **kwargs,
        }

        if protocol.upper() == "TCP":
            data["tcp-portrange"] = port_range
        elif protocol.upper() == "UDP":
            data["udp-portrange"] = port_range

        if comment:
            data["comment"] = comment

        url = f"/pm/config/adom/{adom}/obj/firewall/service/custom"
        await self.client.add(url, data=data)
        return await self.get_service(name, adom=adom)

    async def get_service(self, name: str, adom: str = "root") -> FirewallService:
        """Get specific service.

        Args:
            name: Service name
            adom: ADOM name

        Returns:
            Service details
        """
        url = f"/pm/config/adom/{adom}/obj/firewall/service/custom/{name}"
        data = await self.client.get(url)
        return FirewallService(**data)

    async def delete_service(self, name: str, adom: str = "root") -> None:
        """Delete firewall service.

        Args:
            name: Service name
            adom: ADOM name
        """
        url = f"/pm/config/adom/{adom}/obj/firewall/service/custom/{name}"
        await self.client.delete(url)

    # Phase 18: Metadata Operations
    async def get_object_metadata(
        self,
        object_type: str,
        object_name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get metadata for a firewall object.

        Args:
            object_type: Object type (e.g., "firewall/address", "firewall/service/custom")
            object_name: Object name
            adom: ADOM name

        Returns:
            Object metadata
        """
        url = f"/pm/config/adom/{adom}/obj/{object_type}/{object_name}"
        data = await self.client.get(url, fields=["_meta_fields"])
        return data.get("_meta_fields", {})

    async def set_object_metadata(
        self,
        object_type: str,
        object_name: str,
        metadata: dict[str, Any],
        adom: str = "root",
    ) -> None:
        """Set metadata for a firewall object.

        Args:
            object_type: Object type (e.g., "firewall/address")
            object_name: Object name
            metadata: Metadata key-value pairs
            adom: ADOM name
        """
        url = f"/pm/config/adom/{adom}/obj/{object_type}/{object_name}"
        await self.client.set(url, data={"_meta_fields": metadata})

    async def delete_object_metadata(
        self,
        object_type: str,
        object_name: str,
        metadata_key: str,
        adom: str = "root",
    ) -> None:
        """Delete specific metadata key from an object.

        Args:
            object_type: Object type
            object_name: Object name
            metadata_key: Metadata key to delete
            adom: ADOM name
        """
        # Get current metadata
        current_meta = await self.get_object_metadata(object_type, object_name, adom)
        # Remove the key
        if metadata_key in current_meta:
            del current_meta[metadata_key]
            # Update with remaining metadata
            await self.set_object_metadata(object_type, object_name, current_meta, adom)

    async def assign_object_metadata(
        self,
        object_type: str,
        object_names: list[str],
        metadata_key: str,
        metadata_value: Any,
        adom: str = "root",
    ) -> None:
        """Assign metadata to multiple objects.

        Args:
            object_type: Object type
            object_names: List of object names
            metadata_key: Metadata key
            metadata_value: Metadata value
            adom: ADOM name
        """
        for obj_name in object_names:
            current_meta = await self.get_object_metadata(object_type, obj_name, adom)
            current_meta[metadata_key] = metadata_value
            await self.set_object_metadata(object_type, obj_name, current_meta, adom)

    async def list_objects_by_metadata(
        self,
        object_type: str,
        metadata_key: str,
        metadata_value: Any | None = None,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List objects with specific metadata.

        Args:
            object_type: Object type
            metadata_key: Metadata key to filter by
            metadata_value: Optional metadata value to match
            adom: ADOM name

        Returns:
            List of objects with matching metadata
        """
        url = f"/pm/config/adom/{adom}/obj/{object_type}"
        all_objects = await self.client.get(url, fields=["name", "_meta_fields"])
        
        if not isinstance(all_objects, list):
            all_objects = [all_objects] if all_objects else []
        
        filtered = []
        for obj in all_objects:
            meta = obj.get("_meta_fields", {})
            if metadata_key in meta:
                if metadata_value is None or meta[metadata_key] == metadata_value:
                    filtered.append(obj)
        
        return filtered

    # Phase 18: Where-Used Operations
    async def get_address_where_used(
        self,
        address_name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get where a firewall address is used.

        Args:
            address_name: Address name
            adom: ADOM name

        Returns:
            Usage information (policies, address groups, etc.)
        """
        url = f"/pm/config/adom/{adom}/obj/firewall/address/{address_name}"
        data = {"mkey": address_name}
        result = await self.client.execute(f"{url}/where-used", data=data)
        return result

    async def get_service_where_used(
        self,
        service_name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get where a firewall service is used.

        Args:
            service_name: Service name
            adom: ADOM name

        Returns:
            Usage information
        """
        url = f"/pm/config/adom/{adom}/obj/firewall/service/custom/{service_name}"
        data = {"mkey": service_name}
        result = await self.client.execute(f"{url}/where-used", data=data)
        return result

    async def get_object_dependencies(
        self,
        object_type: str,
        object_name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get dependencies for any object type.

        Args:
            object_type: Object type
            object_name: Object name
            adom: ADOM name

        Returns:
            Dependency information
        """
        url = f"/pm/config/adom/{adom}/obj/{object_type}/{object_name}"
        data = {"mkey": object_name}
        result = await self.client.execute(f"{url}/where-used", data=data)
        return result

    # Phase 18: Zone Management
    async def list_zones(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List firewall zones.

        Args:
            adom: ADOM name

        Returns:
            List of zones
        """
        url = f"/pm/config/adom/{adom}/obj/firewall/zone"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def get_zone(
        self,
        zone_name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get zone details.

        Args:
            zone_name: Zone name
            adom: ADOM name

        Returns:
            Zone details
        """
        url = f"/pm/config/adom/{adom}/obj/firewall/zone/{zone_name}"
        return await self.client.get(url)

    async def create_zone(
        self,
        zone_name: str,
        interfaces: list[str],
        adom: str = "root",
        description: str | None = None,
    ) -> dict[str, Any]:
        """Create firewall zone.

        Args:
            zone_name: Zone name
            interfaces: List of interface names
            adom: ADOM name
            description: Optional description

        Returns:
            Created zone
        """
        data = {
            "name": zone_name,
            "interface": [{"interface-name": iface} for iface in interfaces],
        }
        
        if description:
            data["description"] = description
        
        url = f"/pm/config/adom/{adom}/obj/firewall/zone"
        await self.client.add(url, data=data)
        return await self.get_zone(zone_name, adom)

    async def delete_zone(
        self,
        zone_name: str,
        adom: str = "root",
    ) -> None:
        """Delete firewall zone.

        Args:
            zone_name: Zone name
            adom: ADOM name
        """
        url = f"/pm/config/adom/{adom}/obj/firewall/zone/{zone_name}"
        await self.client.delete(url)

    # Phase 18: Advanced VIP Operations
    async def list_vips(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List virtual IPs (VIPs).

        Args:
            adom: ADOM name

        Returns:
            List of VIPs
        """
        url = f"/pm/config/adom/{adom}/obj/firewall/vip"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def get_vip(
        self,
        vip_name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get VIP details.

        Args:
            vip_name: VIP name
            adom: ADOM name

        Returns:
            VIP details
        """
        url = f"/pm/config/adom/{adom}/obj/firewall/vip/{vip_name}"
        return await self.client.get(url)

    async def create_vip(
        self,
        vip_name: str,
        external_ip: str,
        mapped_ip: str,
        adom: str = "root",
        external_interface: str | None = None,
        port_forward: bool = False,
        external_port: str | None = None,
        mapped_port: str | None = None,
        protocol: str = "tcp",
        comment: str | None = None,
    ) -> dict[str, Any]:
        """Create virtual IP (VIP).

        Args:
            vip_name: VIP name
            external_ip: External IP address
            mapped_ip: Mapped internal IP
            adom: ADOM name
            external_interface: External interface name
            port_forward: Enable port forwarding
            external_port: External port (if port forwarding)
            mapped_port: Mapped port (if port forwarding)
            protocol: Protocol (tcp/udp)
            comment: Optional comment

        Returns:
            Created VIP
        """
        data = {
            "name": vip_name,
            "extip": external_ip,
            "mappedip": [[mapped_ip, mapped_ip]],
            "type": "static-nat",
        }
        
        if external_interface:
            data["extintf"] = external_interface
        
        if port_forward and external_port and mapped_port:
            data["portforward"] = "enable"
            data["protocol"] = protocol
            data["extport"] = external_port
            data["mappedport"] = mapped_port
        
        if comment:
            data["comment"] = comment
        
        url = f"/pm/config/adom/{adom}/obj/firewall/vip"
        await self.client.add(url, data=data)
        return await self.get_vip(vip_name, adom)

    async def delete_vip(
        self,
        vip_name: str,
        adom: str = "root",
    ) -> None:
        """Delete virtual IP.

        Args:
            vip_name: VIP name
            adom: ADOM name
        """
        url = f"/pm/config/adom/{adom}/obj/firewall/vip/{vip_name}"
        await self.client.delete(url)

    # =========================================================================
    # Phase 21: Dynamic Objects
    # =========================================================================

    async def list_dynamic_addresses(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List dynamic firewall addresses.
        
        Dynamic addresses can be automatically updated by FortiGate based on
        cloud connectors, SDN connectors, or other dynamic sources.

        Args:
            adom: ADOM name

        Returns:
            List of dynamic addresses
        """
        url = f"/pm/config/adom/{adom}/obj/firewall/address"
        data = await self.client.get(url)
        addresses = data if isinstance(data, list) else [data] if data else []
        
        # Filter for dynamic type addresses
        dynamic = [addr for addr in addresses if addr.get("type") in ["dynamic", "mac"]]
        return dynamic

    async def list_fabric_connector_addresses(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List Fabric connector addresses.
        
        Fabric connector addresses are dynamically populated from cloud
        providers (AWS, Azure, GCP) or SDN controllers.

        Args:
            adom: ADOM name

        Returns:
            List of Fabric connector addresses
        """
        url = f"/pm/config/adom/{adom}/obj/firewall/address"
        data = await self.client.get(url)
        addresses = data if isinstance(data, list) else [data] if data else []
        
        # Filter for fabric connector type
        fabric = [addr for addr in addresses if addr.get("sdn") or addr.get("fsso-group")]
        return fabric

    async def get_address_filters(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List address filters for dynamic updates.
        
        Address filters define criteria for automatically including/excluding
        addresses from dynamic groups based on tags, metadata, or attributes.

        Args:
            adom: ADOM name

        Returns:
            List of address filters
        """
        url = f"/pm/config/adom/{adom}/obj/firewall/addrgrp"
        data = await self.client.get(url)
        groups = data if isinstance(data, list) else [data] if data else []
        
        # Extract groups with filters
        filtered = [grp for grp in groups if grp.get("type") == "dynamic"]
        return filtered

    # =========================================================================
    # Phase 21: Interface Objects
    # =========================================================================

    async def list_interface_addresses(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List interface-based addresses.
        
        Interface addresses reference FortiGate interfaces directly
        and use the interface's IP as the address.

        Args:
            adom: ADOM name

        Returns:
            List of interface addresses
        """
        url = f"/pm/config/adom/{adom}/obj/firewall/address"
        data = await self.client.get(url)
        addresses = data if isinstance(data, list) else [data] if data else []
        
        # Filter for interface type
        interface_addrs = [addr for addr in addresses if addr.get("type") == "interface-subnet"]
        return interface_addrs

    async def list_wildcard_fqdn_addresses(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List wildcard FQDN addresses.
        
        Wildcard FQDN addresses match domain patterns (e.g., *.google.com)
        and are resolved dynamically by FortiGate DNS lookups.

        Args:
            adom: ADOM name

        Returns:
            List of wildcard FQDN addresses
        """
        url = f"/pm/config/adom/{adom}/obj/firewall/address"
        data = await self.client.get(url)
        addresses = data if isinstance(data, list) else [data] if data else []
        
        # Filter for wildcard FQDN type
        fqdn_addrs = [addr for addr in addresses if addr.get("type") == "wildcard-fqdn"]
        return fqdn_addrs

    async def list_geography_addresses(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List geography-based addresses.
        
        Geography addresses represent countries or regions and are used
        for geo-blocking or geo-routing policies.

        Args:
            adom: ADOM name

        Returns:
            List of geography addresses
        """
        url = f"/pm/config/adom/{adom}/obj/firewall/address"
        data = await self.client.get(url)
        addresses = data if isinstance(data, list) else [data] if data else []
        
        # Filter for geography type
        geo_addrs = [addr for addr in addresses if addr.get("type") == "geography"]
        return geo_addrs

    # =========================================================================
    # Phase 21: Multicast Objects
    # =========================================================================

    async def list_multicast_addresses(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List multicast addresses.
        
        Multicast addresses are used in multicast policies for
        group communication protocols (e.g., IPTV, video conferencing).

        Args:
            adom: ADOM name

        Returns:
            List of multicast addresses
        """
        url = f"/pm/config/adom/{adom}/obj/firewall/multicast-address"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def get_multicast_address(
        self,
        name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get multicast address details.
        
        Retrieves configuration of a specific multicast address including
        start IP, end IP, and associated interfaces.

        Args:
            name: Multicast address name
            adom: ADOM name

        Returns:
            Multicast address details
        """
        url = f"/pm/config/adom/{adom}/obj/firewall/multicast-address/{name}"
        data = await self.client.get(url)
        return data if isinstance(data, dict) else {}

    # =========================================================================
    # Phase 26: Complete Objects Management
    # =========================================================================

    async def list_service_categories(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List service categories.
        
        Service categories group related services together (e.g., Email,
        Web Access, Remote Access) for easier policy management.

        Args:
            adom: ADOM name

        Returns:
            List of service categories
        """
        url = f"/pm/config/adom/{adom}/obj/firewall/service/category"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def list_proxy_addresses(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List proxy addresses.
        
        Proxy addresses are used in explicit web proxy policies to match
        URLs, hosts, methods, and user agents for granular HTTP/HTTPS control.

        Args:
            adom: ADOM name

        Returns:
            List of proxy addresses
        """
        url = f"/pm/config/adom/{adom}/obj/firewall/proxy-address"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    # =========================================================================
    # Phase 44: Additional Object Operations
    # =========================================================================

    async def list_ipv6_addresses(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List IPv6 firewall addresses.
        
        Args:
            adom: ADOM name
            
        Returns:
            List of IPv6 addresses
        """
        url = f"/pm/config/adom/{adom}/obj/firewall/address6"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def list_ipv6_address_groups(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List IPv6 address groups.
        
        Args:
            adom: ADOM name
            
        Returns:
            List of IPv6 address groups
        """
        url = f"/pm/config/adom/{adom}/obj/firewall/addrgrp6"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def list_schedules(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List firewall schedules.
        
        Args:
            adom: ADOM name
            
        Returns:
            List of schedules
        """
        url = f"/pm/config/adom/{adom}/obj/firewall/schedule/onetime"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def list_recurring_schedules(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List recurring firewall schedules.
        
        Args:
            adom: ADOM name
            
        Returns:
            List of recurring schedules
        """
        url = f"/pm/config/adom/{adom}/obj/firewall/schedule/recurring"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def list_internet_services(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List internet service definitions.
        
        Args:
            adom: ADOM name
            
        Returns:
            List of internet services
        """
        url = f"/pm/config/adom/{adom}/obj/firewall/internet-service-custom"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def list_shaping_profiles(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List traffic shaping profiles.
        
        Args:
            adom: ADOM name
            
        Returns:
            List of shaping profiles
        """
        url = f"/pm/config/adom/{adom}/obj/firewall/shaping-profile"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def list_traffic_shapers(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List traffic shapers.
        
        Args:
            adom: ADOM name
            
        Returns:
            List of traffic shapers
        """
        url = f"/pm/config/adom/{adom}/obj/firewall/shaper/traffic-shaper"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    # =========================================================================
    # Phase 48: Advanced Object Types
    # =========================================================================

    async def list_internet_service_fqdns(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List Internet Service FQDN definitions.
        
        Internet Service FQDNs allow matching traffic based on fully qualified
        domain names that are part of cloud/internet services. Used for:
        - Cloud application identification
        - SaaS service control
        - Dynamic service matching
        
        Args:
            adom: ADOM name
            
        Returns:
            List of Internet Service FQDN definitions
        """
        url = f"/pm/config/adom/{adom}/obj/firewall/internet-service-name"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def create_internet_service_fqdn(
        self,
        name: str,
        internet_service_id: int,
        adom: str = "root",
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Create Internet Service FQDN definition.
        
        Associates an FQDN pattern with an Internet Service ID for dynamic
        service matching.
        
        Args:
            name: FQDN definition name
            internet_service_id: FortiGuard Internet Service ID
            adom: ADOM name
            **kwargs: Additional parameters (type, server-name, etc.)
            
        Returns:
            Created Internet Service FQDN
            
        Example:
            create_internet_service_fqdn(
                name="office365-fqdn",
                internet_service_id=65536,
                adom="root"
            )
        """
        data = {
            "name": name,
            "internet-service-id": internet_service_id,
            **kwargs,
        }
        url = f"/pm/config/adom/{adom}/obj/firewall/internet-service-name"
        return await self.client.add(url, data=data)

    async def delete_internet_service_fqdn(
        self,
        name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Delete Internet Service FQDN definition.
        
        Args:
            name: FQDN definition name to delete
            adom: ADOM name
            
        Returns:
            Deletion result
        """
        url = f"/pm/config/adom/{adom}/obj/firewall/internet-service-name/{name}"
        return await self.client.delete(url)

    async def get_normalized_interface_mappings(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """Get normalized interface mappings.
        
        Retrieves platform-specific interface name mappings to normalized names.
        Useful for:
        - Multi-platform policy deployment
        - Interface abstraction
        - Cross-device consistency
        
        Normalized interfaces allow policies to reference generic interface names
        (e.g., "wan1", "lan1") that map to actual physical interfaces on different
        device models.
        
        Args:
            adom: ADOM name
            
        Returns:
            List of interface mappings with platform-specific translations
        """
        url = f"/pm/config/adom/{adom}/obj/dynamic/interface"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def list_replacement_message_groups(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List replacement message groups.
        
        Replacement message groups customize the messages displayed to users
        when traffic is blocked or content is filtered. Used for:
        - Custom block pages (HTTP/HTTPS)
        - Authentication pages
        - Disclaimer messages
        - Virus/malware notifications
        - User communication customization
        
        Args:
            adom: ADOM name
            
        Returns:
            List of replacement message groups
        """
        url = f"/pm/config/adom/{adom}/obj/system/replacemsg-group"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def list_virtual_wire_pairs(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List virtual wire pair configurations.
        
        Virtual wire pairs create transparent layer-2 connections between two
        interfaces, operating in tap or transparent mode. Used for:
        - Inline security inspection
        - Transparent firewall deployment
        - Traffic monitoring
        - IPS/IDS deployment
        
        Virtual wire pairs pass traffic between interfaces without requiring
        IP addresses or routing configuration.
        
        Args:
            adom: ADOM name
            
        Returns:
            List of virtual wire pair configurations
        """
        url = f"/pm/config/adom/{adom}/obj/firewall/vwpair"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

