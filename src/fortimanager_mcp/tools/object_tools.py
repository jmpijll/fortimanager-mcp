"""MCP tools for firewall object management operations."""

import logging
from typing import Any

from fortimanager_mcp.api.objects import ObjectAPI
from fortimanager_mcp.server import get_fmg_client, mcp

logger = logging.getLogger(__name__)


def _get_object_api() -> ObjectAPI:
    """Get ObjectAPI instance."""
    client = get_fmg_client()
    if not client:
        raise RuntimeError("FortiManager client not initialized")
    return ObjectAPI(client)


@mcp.tool()
async def list_firewall_addresses(
    adom: str = "root",
    filter_name: str | None = None,
) -> dict[str, Any]:
    """List firewall address objects in an ADOM.

    Retrieves all firewall address objects that can be used in policies.
    Address objects define IP addresses, subnets, ranges, or FQDNs.

    Args:
        adom: ADOM name (default: "root")
        filter_name: Optional filter to match address names

    Returns:
        Dictionary with list of firewall addresses

    Example:
        # List all addresses
        result = list_firewall_addresses(adom="root")

        # Filter by name
        result = list_firewall_addresses(adom="root", filter_name="internal")
    """
    try:
        api = _get_object_api()

        filter_criteria = None
        if filter_name:
            filter_criteria = ["name", "like", filter_name]

        addresses = await api.list_addresses(adom=adom, filter=filter_criteria)

        return {
            "status": "success",
            "count": len(addresses),
            "addresses": [
                {
                    "name": addr.name,
                    "type": addr.type,
                    "subnet": addr.subnet,
                    "fqdn": addr.fqdn,
                    "comment": addr.comment,
                }
                for addr in addresses
            ],
        }
    except Exception as e:
        logger.error(f"Error listing addresses in ADOM {adom}: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def create_firewall_address(
    name: str,
    subnet: str,
    adom: str = "root",
    comment: str | None = None,
) -> dict[str, Any]:
    """Create a new firewall address object.

    Creates a subnet-type firewall address object that can be used in
    firewall policies and other security configurations.

    Args:
        name: Unique name for the address object
        subnet: IP address and netmask in CIDR format (e.g., "192.168.1.0/24")
        adom: ADOM name (default: "root")
        comment: Optional description

    Returns:
        Dictionary with created address details

    Example:
        result = create_firewall_address(
            name="internal_network",
            subnet="10.0.0.0/8",
            adom="root",
            comment="RFC1918 internal network"
        )
    """
    try:
        api = _get_object_api()
        address = await api.create_address(
            name=name,
            subnet=subnet,
            adom=adom,
            comment=comment,
        )

        return {
            "status": "success",
            "message": f"Address '{name}' created successfully",
            "address": {
                "name": address.name,
                "type": address.type,
                "subnet": address.subnet,
                "comment": address.comment,
            },
        }
    except Exception as e:
        logger.error(f"Error creating address {name}: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def update_firewall_address(
    name: str,
    adom: str = "root",
    comment: str | None = None,
    **kwargs: Any,
) -> dict[str, Any]:
    """Update an existing firewall address object.

    Modifies properties of an existing address object.
    Only specified fields will be updated.

    Args:
        name: Address name
        adom: ADOM name (default: "root")
        comment: Updated comment
        **kwargs: Additional fields to update

    Returns:
        Dictionary with updated address details

    Example:
        result = update_firewall_address(
            name="internal_network",
            adom="root",
            comment="Updated description"
        )
    """
    try:
        api = _get_object_api()

        update_data = {**kwargs}
        if comment is not None:
            update_data["comment"] = comment

        address = await api.update_address(name=name, adom=adom, **update_data)

        return {
            "status": "success",
            "message": f"Address '{name}' updated successfully",
            "address": {
                "name": address.name,
                "type": address.type,
                "subnet": address.subnet,
                "comment": address.comment,
            },
        }
    except Exception as e:
        logger.error(f"Error updating address {name}: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def delete_firewall_address(name: str, adom: str = "root") -> dict[str, Any]:
    """Delete a firewall address object.

    Removes an address object from FortiManager.
    Address must not be in use by any policies or address groups.

    Args:
        name: Address name
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with deletion status

    Example:
        result = delete_firewall_address(name="internal_network", adom="root")
    """
    try:
        api = _get_object_api()
        await api.delete_address(name=name, adom=adom)

        return {
            "status": "success",
            "message": f"Address '{name}' deleted successfully",
        }
    except Exception as e:
        logger.error(f"Error deleting address {name}: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def list_address_groups(adom: str = "root") -> dict[str, Any]:
    """List firewall address groups in an ADOM.

    Retrieves all address group objects that contain multiple addresses.
    Address groups simplify policy management by grouping related addresses.

    Args:
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with list of address groups

    Example:
        result = list_address_groups(adom="root")
    """
    try:
        api = _get_object_api()
        groups = await api.list_address_groups(adom=adom)

        return {
            "status": "success",
            "count": len(groups),
            "groups": [
                {
                    "name": grp.name,
                    "members": grp.member,
                    "comment": grp.comment,
                }
                for grp in groups
            ],
        }
    except Exception as e:
        logger.error(f"Error listing address groups in ADOM {adom}: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def create_address_group(
    name: str,
    members: list[str],
    adom: str = "root",
    comment: str | None = None,
) -> dict[str, Any]:
    """Create a new firewall address group.

    Creates a group containing multiple address objects.
    All member addresses must exist before creating the group.

    Args:
        name: Group name
        members: List of address object names to include
        adom: ADOM name (default: "root")
        comment: Optional description

    Returns:
        Dictionary with created group details

    Example:
        result = create_address_group(
            name="internal_networks",
            members=["network_a", "network_b", "network_c"],
            adom="root",
            comment="All internal networks"
        )
    """
    try:
        api = _get_object_api()
        group = await api.create_address_group(
            name=name,
            members=members,
            adom=adom,
            comment=comment,
        )

        return {
            "status": "success",
            "message": f"Address group '{name}' created successfully",
            "group": {
                "name": group.name,
                "members": group.member,
                "comment": group.comment,
            },
        }
    except Exception as e:
        logger.error(f"Error creating address group {name}: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def list_firewall_services(adom: str = "root") -> dict[str, Any]:
    """List firewall service objects in an ADOM.

    Retrieves all custom service objects that define TCP/UDP ports or ICMP types.
    Services are used in firewall policies to control application access.

    Args:
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with list of services

    Example:
        result = list_firewall_services(adom="root")
    """
    try:
        api = _get_object_api()
        services = await api.list_services(adom=adom)

        return {
            "status": "success",
            "count": len(services),
            "services": [
                {
                    "name": svc.name,
                    "protocol": svc.protocol,
                    "tcp_ports": svc.tcp_portrange,
                    "udp_ports": svc.udp_portrange,
                    "comment": svc.comment,
                }
                for svc in services
            ],
        }
    except Exception as e:
        logger.error(f"Error listing services in ADOM {adom}: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def create_firewall_service(
    name: str,
    protocol: str,
    port_range: str,
    adom: str = "root",
    comment: str | None = None,
) -> dict[str, Any]:
    """Create a new firewall service object.

    Creates a custom service object defining TCP or UDP ports.
    Services can specify single ports or ranges.

    Args:
        name: Service name
        protocol: Protocol (TCP or UDP)
        port_range: Port or port range (e.g., "80" or "8000-8080")
        adom: ADOM name (default: "root")
        comment: Optional description

    Returns:
        Dictionary with created service details

    Example:
        result = create_firewall_service(
            name="web_alt",
            protocol="TCP",
            port_range="8080",
            adom="root",
            comment="Alternative web server port"
        )
    """
    try:
        api = _get_object_api()
        service = await api.create_service(
            name=name,
            protocol=protocol,
            port_range=port_range,
            adom=adom,
            comment=comment,
        )

        return {
            "status": "success",
            "message": f"Service '{name}' created successfully",
            "service": {
                "name": service.name,
                "protocol": service.protocol,
                "tcp_ports": service.tcp_portrange,
                "udp_ports": service.udp_portrange,
                "comment": service.comment,
            },
        }
    except Exception as e:
        logger.error(f"Error creating service {name}: {e}")
        return {"status": "error", "message": str(e)}


# ============================================================================
# Phase 18: Objects Management - Metadata Operations
# ============================================================================


@mcp.tool()
async def get_object_metadata(
    object_type: str,
    object_name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Get metadata for a firewall object.

    Retrieves custom metadata tags and values associated with any firewall object.
    Metadata is used for organization, automation, and custom workflows.

    Args:
        object_type: Object type (e.g., "firewall/address", "firewall/service/custom")
        object_name: Object name
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with metadata key-value pairs

    Example:
        result = get_object_metadata(
            object_type="firewall/address",
            object_name="Corporate-Network",
            adom="root"
        )
    """
    try:
        client = get_fmg_client()
        if not client:
            raise RuntimeError("FortiManager client not initialized")

        api = ObjectAPI(client)
        metadata = await api.get_object_metadata(object_type, object_name, adom)

        return {
            "status": "success",
            "object_type": object_type,
            "object_name": object_name,
            "metadata": metadata,
        }
    except Exception as e:
        logger.error(f"Error getting object metadata: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def set_object_metadata(
    object_type: str,
    object_name: str,
    metadata_key: str,
    metadata_value: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Set metadata for a firewall object.

    Adds or updates custom metadata tags on firewall objects.
    Useful for categorization, compliance tracking, and automation.

    Args:
        object_type: Object type (e.g., "firewall/address")
        object_name: Object name
        metadata_key: Metadata key name
        metadata_value: Metadata value
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with operation status

    Example:
        result = set_object_metadata(
            object_type="firewall/address",
            object_name="Corporate-Network",
            metadata_key="environment",
            metadata_value="production",
            adom="root"
        )
    """
    try:
        client = get_fmg_client()
        if not client:
            raise RuntimeError("FortiManager client not initialized")

        api = ObjectAPI(client)
        
        # Get current metadata
        current_meta = await api.get_object_metadata(object_type, object_name, adom)
        current_meta[metadata_key] = metadata_value
        
        # Set updated metadata
        await api.set_object_metadata(object_type, object_name, current_meta, adom)

        return {
            "status": "success",
            "message": f"Metadata '{metadata_key}' set on {object_name}",
        }
    except Exception as e:
        logger.error(f"Error setting object metadata: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def delete_object_metadata(
    object_type: str,
    object_name: str,
    metadata_key: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Delete specific metadata from a firewall object.

    Removes a metadata key and its value from an object.

    Args:
        object_type: Object type
        object_name: Object name
        metadata_key: Metadata key to delete
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with operation status

    Example:
        result = delete_object_metadata(
            object_type="firewall/address",
            object_name="Corporate-Network",
            metadata_key="old_environment",
            adom="root"
        )
    """
    try:
        client = get_fmg_client()
        if not client:
            raise RuntimeError("FortiManager client not initialized")

        api = ObjectAPI(client)
        await api.delete_object_metadata(object_type, object_name, metadata_key, adom)

        return {
            "status": "success",
            "message": f"Metadata '{metadata_key}' deleted from {object_name}",
        }
    except Exception as e:
        logger.error(f"Error deleting object metadata: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def assign_metadata_to_objects(
    object_type: str,
    object_names: list[str],
    metadata_key: str,
    metadata_value: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Assign metadata to multiple objects at once.

    Bulk operation to tag multiple objects with the same metadata.
    Useful for categorizing groups of objects.

    Args:
        object_type: Object type
        object_names: List of object names
        metadata_key: Metadata key
        metadata_value: Metadata value
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with operation status

    Example:
        result = assign_metadata_to_objects(
            object_type="firewall/address",
            object_names=["Server1", "Server2", "Server3"],
            metadata_key="datacenter",
            metadata_value="DC1",
            adom="root"
        )
    """
    try:
        client = get_fmg_client()
        if not client:
            raise RuntimeError("FortiManager client not initialized")

        api = ObjectAPI(client)
        await api.assign_object_metadata(
            object_type, object_names, metadata_key, metadata_value, adom
        )

        return {
            "status": "success",
            "message": f"Metadata assigned to {len(object_names)} objects",
            "objects_updated": object_names,
        }
    except Exception as e:
        logger.error(f"Error assigning metadata: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def list_objects_by_metadata(
    object_type: str,
    metadata_key: str,
    metadata_value: str | None = None,
    adom: str = "root",
) -> dict[str, Any]:
    """List objects filtered by metadata.

    Finds all objects that have specific metadata tags.
    Useful for finding all objects in a category or with specific attributes.

    Args:
        object_type: Object type
        metadata_key: Metadata key to filter by
        metadata_value: Optional metadata value to match
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with list of matching objects

    Example:
        # Find all production addresses
        result = list_objects_by_metadata(
            object_type="firewall/address",
            metadata_key="environment",
            metadata_value="production",
            adom="root"
        )
    """
    try:
        client = get_fmg_client()
        if not client:
            raise RuntimeError("FortiManager client not initialized")

        api = ObjectAPI(client)
        objects = await api.list_objects_by_metadata(
            object_type, metadata_key, metadata_value, adom
        )

        return {
            "status": "success",
            "count": len(objects),
            "objects": objects,
        }
    except Exception as e:
        logger.error(f"Error listing objects by metadata: {e}")
        return {"status": "error", "message": str(e)}


# ============================================================================
# Phase 18: Objects Management - Where-Used Operations  
# ============================================================================


@mcp.tool()
async def get_address_where_used(
    address_name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Get where a firewall address is used.

    Shows all policies, address groups, and other locations where an address
    object is referenced. Essential before deleting or modifying addresses.

    Args:
        address_name: Address name to check
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with usage information

    Example:
        result = get_address_where_used(
            address_name="Corporate-Network",
            adom="root"
        )
    """
    try:
        client = get_fmg_client()
        if not client:
            raise RuntimeError("FortiManager client not initialized")

        api = ObjectAPI(client)
        usage = await api.get_address_where_used(address_name, adom)

        return {
            "status": "success",
            "address_name": address_name,
            "usage": usage,
        }
    except Exception as e:
        logger.error(f"Error getting address where-used: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_service_where_used(
    service_name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Get where a firewall service is used.

    Shows all policies and other locations where a service object is referenced.
    Use this before deleting or modifying services.

    Args:
        service_name: Service name to check
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with usage information

    Example:
        result = get_service_where_used(
            service_name="HTTP-8080",
            adom="root"
        )
    """
    try:
        client = get_fmg_client()
        if not client:
            raise RuntimeError("FortiManager client not initialized")

        api = ObjectAPI(client)
        usage = await api.get_service_where_used(service_name, adom)

        return {
            "status": "success",
            "service_name": service_name,
            "usage": usage,
        }
    except Exception as e:
        logger.error(f"Error getting service where-used: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_object_dependencies(
    object_type: str,
    object_name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Get dependencies for any object type.

    Universal where-used checker that works for any firewall object type.
    Shows all dependencies and references.

    Args:
        object_type: Object type (e.g., "firewall/address", "firewall/addrgrp")
        object_name: Object name
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with dependency information

    Example:
        result = get_object_dependencies(
            object_type="firewall/addrgrp",
            object_name="Web-Servers",
            adom="root"
        )
    """
    try:
        client = get_fmg_client()
        if not client:
            raise RuntimeError("FortiManager client not initialized")

        api = ObjectAPI(client)
        dependencies = await api.get_object_dependencies(object_type, object_name, adom)

        return {
            "status": "success",
            "object_type": object_type,
            "object_name": object_name,
            "dependencies": dependencies,
        }
    except Exception as e:
        logger.error(f"Error getting object dependencies: {e}")
        return {"status": "error", "message": str(e)}


# ============================================================================
# Phase 18: Objects Management - Zone Management
# ============================================================================


@mcp.tool()
async def list_firewall_zones(adom: str = "root") -> dict[str, Any]:
    """List all firewall zones.

    Zones group interfaces for simplified policy creation.
    This retrieves all configured zones in the ADOM.

    Args:
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with list of zones

    Example:
        result = list_firewall_zones(adom="root")
    """
    try:
        client = get_fmg_client()
        if not client:
            raise RuntimeError("FortiManager client not initialized")

        api = ObjectAPI(client)
        zones = await api.list_zones(adom)

        return {
            "status": "success",
            "count": len(zones),
            "zones": zones,
        }
    except Exception as e:
        logger.error(f"Error listing zones: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_firewall_zone(
    zone_name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Get firewall zone details.

    Retrieves detailed information about a specific zone including
    its member interfaces.

    Args:
        zone_name: Zone name
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with zone details

    Example:
        result = get_firewall_zone(
            zone_name="internal-zone",
            adom="root"
        )
    """
    try:
        client = get_fmg_client()
        if not client:
            raise RuntimeError("FortiManager client not initialized")

        api = ObjectAPI(client)
        zone = await api.get_zone(zone_name, adom)

        return {
            "status": "success",
            "zone": zone,
        }
    except Exception as e:
        logger.error(f"Error getting zone: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def create_firewall_zone(
    zone_name: str,
    interfaces: list[str],
    adom: str = "root",
    description: str | None = None,
) -> dict[str, Any]:
    """Create a new firewall zone.

    Creates a zone grouping multiple interfaces together.
    Zones simplify policy creation by allowing policies to reference
    zones instead of individual interfaces.

    Args:
        zone_name: Zone name
        interfaces: List of interface names to include
        adom: ADOM name (default: "root")
        description: Optional description

    Returns:
        Dictionary with created zone details

    Example:
        result = create_firewall_zone(
            zone_name="dmz-zone",
            interfaces=["port3", "port4"],
            description="DMZ network zone",
            adom="root"
        )
    """
    try:
        client = get_fmg_client()
        if not client:
            raise RuntimeError("FortiManager client not initialized")

        api = ObjectAPI(client)
        zone = await api.create_zone(zone_name, interfaces, adom, description)

        return {
            "status": "success",
            "message": f"Zone '{zone_name}' created successfully",
            "zone": zone,
        }
    except Exception as e:
        logger.error(f"Error creating zone: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def delete_firewall_zone(
    zone_name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Delete a firewall zone.

    Removes a zone configuration. Zone must not be referenced
    in any policies before deletion.

    Args:
        zone_name: Zone name to delete
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with operation status

    Example:
        result = delete_firewall_zone(
            zone_name="old-dmz-zone",
            adom="root"
        )
    """
    try:
        client = get_fmg_client()
        if not client:
            raise RuntimeError("FortiManager client not initialized")

        api = ObjectAPI(client)
        await api.delete_zone(zone_name, adom)

        return {
            "status": "success",
            "message": f"Zone '{zone_name}' deleted successfully",
        }
    except Exception as e:
        logger.error(f"Error deleting zone: {e}")
        return {"status": "error", "message": str(e)}


# ============================================================================
# Phase 18: Objects Management - Advanced VIP Operations
# ============================================================================


@mcp.tool()
async def list_virtual_ips(adom: str = "root") -> dict[str, Any]:
    """List all virtual IP (VIP) objects.

    VIPs are used for port forwarding and load balancing,
    mapping external IPs to internal servers.

    Args:
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with list of VIPs

    Example:
        result = list_virtual_ips(adom="root")
    """
    try:
        client = get_fmg_client()
        if not client:
            raise RuntimeError("FortiManager client not initialized")

        api = ObjectAPI(client)
        vips = await api.list_vips(adom)

        return {
            "status": "success",
            "count": len(vips),
            "vips": vips,
        }
    except Exception as e:
        logger.error(f"Error listing VIPs: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_virtual_ip(
    vip_name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Get virtual IP (VIP) details.

    Retrieves detailed configuration of a specific VIP object.

    Args:
        vip_name: VIP name
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with VIP details

    Example:
        result = get_virtual_ip(
            vip_name="web-server-vip",
            adom="root"
        )
    """
    try:
        client = get_fmg_client()
        if not client:
            raise RuntimeError("FortiManager client not initialized")

        api = ObjectAPI(client)
        vip = await api.get_vip(vip_name, adom)

        return {
            "status": "success",
            "vip": vip,
        }
    except Exception as e:
        logger.error(f"Error getting VIP: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def create_virtual_ip(
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
    """Create a virtual IP (VIP) object.

    Creates a VIP for port forwarding or load balancing.
    Maps an external IP (optionally with port) to an internal server.

    Args:
        vip_name: VIP name
        external_ip: External/public IP address
        mapped_ip: Internal/private IP address
        adom: ADOM name (default: "root")
        external_interface: External interface name
        port_forward: Enable port forwarding
        external_port: External port (e.g., "8080" or "8080-8090")
        mapped_port: Internal port (e.g., "80" or "80-90")
        protocol: Protocol (tcp/udp, default: tcp)
        comment: Optional comment

    Returns:
        Dictionary with created VIP details

    Example:
        # Simple NAT
        result = create_virtual_ip(
            vip_name="web-server-vip",
            external_ip="203.0.113.10",
            mapped_ip="192.168.1.100",
            adom="root"
        )

        # Port forwarding
        result = create_virtual_ip(
            vip_name="ssh-server-vip",
            external_ip="203.0.113.10",
            mapped_ip="192.168.1.50",
            port_forward=True,
            external_port="2222",
            mapped_port="22",
            protocol="tcp",
            adom="root"
        )
    """
    try:
        client = get_fmg_client()
        if not client:
            raise RuntimeError("FortiManager client not initialized")

        api = ObjectAPI(client)
        vip = await api.create_vip(
            vip_name=vip_name,
            external_ip=external_ip,
            mapped_ip=mapped_ip,
            adom=adom,
            external_interface=external_interface,
            port_forward=port_forward,
            external_port=external_port,
            mapped_port=mapped_port,
            protocol=protocol,
            comment=comment,
        )

        return {
            "status": "success",
            "message": f"VIP '{vip_name}' created successfully",
            "vip": vip,
        }
    except Exception as e:
        logger.error(f"Error creating VIP: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def delete_virtual_ip(
    vip_name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Delete a virtual IP (VIP) object.

    Removes a VIP configuration. Check where-used before deleting
    to avoid breaking policies.

    Args:
        vip_name: VIP name to delete
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with operation status

    Example:
        result = delete_virtual_ip(
            vip_name="old-vip",
            adom="root"
        )
    """
    try:
        client = get_fmg_client()
        if not client:
            raise RuntimeError("FortiManager client not initialized")

        api = ObjectAPI(client)
        await api.delete_vip(vip_name, adom)

        return {
            "status": "success",
            "message": f"VIP '{vip_name}' deleted successfully",
        }
    except Exception as e:
        logger.error(f"Error deleting VIP: {e}")
        return {"status": "error", "message": str(e)}


# ============================================================================
# Phase 21: Advanced Objects - Dynamic Objects
# ============================================================================


@mcp.tool()
async def list_dynamic_firewall_addresses(adom: str = "root") -> dict[str, Any]:
    """List dynamic firewall addresses.
    
    Dynamic addresses are automatically updated by FortiGate based on:
    - Cloud connectors (AWS, Azure, GCP)
    - SDN connectors (VMware NSX, Cisco ACI)
    - MAC addresses (for endpoint visibility)
    - FSSO groups (Fortinet Single Sign-On)
    
    Args:
        adom: ADOM name (default: "root")
    
    Returns:
        Dictionary with list of dynamic addresses
    
    Example:
        result = list_dynamic_firewall_addresses(adom="root")
    """
    try:
        client = get_fmg_client()
        if not client:
            raise RuntimeError("FortiManager client not initialized")
        
        api = ObjectAPI(client)
        addresses = await api.list_dynamic_addresses(adom)
        
        return {
            "status": "success",
            "count": len(addresses),
            "addresses": addresses,
        }
    except Exception as e:
        logger.error(f"Error listing dynamic addresses: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def list_fabric_connector_addresses(adom: str = "root") -> dict[str, Any]:
    """List Fabric connector addresses.
    
    Fabric connector addresses are automatically populated from:
    - AWS EC2 instances (by tag, VPC, region)
    - Azure virtual machines (by resource group, tags)
    - Google Cloud Compute instances
    - VMware vCenter VMs
    - Kubernetes pods and services
    
    These addresses update automatically as cloud resources change.
    
    Args:
        adom: ADOM name (default: "root")
    
    Returns:
        Dictionary with list of Fabric connector addresses
    
    Example:
        result = list_fabric_connector_addresses(adom="root")
    """
    try:
        client = get_fmg_client()
        if not client:
            raise RuntimeError("FortiManager client not initialized")
        
        api = ObjectAPI(client)
        addresses = await api.list_fabric_connector_addresses(adom)
        
        return {
            "status": "success",
            "count": len(addresses),
            "addresses": addresses,
        }
    except Exception as e:
        logger.error(f"Error listing Fabric connector addresses: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def list_address_filters(adom: str = "root") -> dict[str, Any]:
    """List address group filters for dynamic membership.
    
    Address filters define dynamic group membership based on:
    - Tags (environment=production, team=engineering)
    - Metadata attributes
    - Geographic location
    - SDN connector filters
    
    Objects matching filter criteria are automatically added/removed
    from the address group as they are created or modified.
    
    Args:
        adom: ADOM name (default: "root")
    
    Returns:
        Dictionary with list of dynamic address groups with filters
    
    Example:
        result = list_address_filters(adom="root")
    """
    try:
        client = get_fmg_client()
        if not client:
            raise RuntimeError("FortiManager client not initialized")
        
        api = ObjectAPI(client)
        filters = await api.get_address_filters(adom)
        
        return {
            "status": "success",
            "count": len(filters),
            "filters": filters,
        }
    except Exception as e:
        logger.error(f"Error listing address filters: {e}")
        return {"status": "error", "message": str(e)}


# ============================================================================
# Phase 21: Advanced Objects - Interface Objects
# ============================================================================


@mcp.tool()
async def list_interface_addresses(adom: str = "root") -> dict[str, Any]:
    """List interface-based addresses.
    
    Interface addresses reference FortiGate interfaces and use
    the interface's IP address automatically. These are useful for:
    - Policy objects that follow interface IP changes
    - HA configurations
    - DHCP-assigned interfaces
    
    Args:
        adom: ADOM name (default: "root")
    
    Returns:
        Dictionary with list of interface-based addresses
    
    Example:
        result = list_interface_addresses(adom="root")
    """
    try:
        client = get_fmg_client()
        if not client:
            raise RuntimeError("FortiManager client not initialized")
        
        api = ObjectAPI(client)
        addresses = await api.list_interface_addresses(adom)
        
        return {
            "status": "success",
            "count": len(addresses),
            "addresses": addresses,
        }
    except Exception as e:
        logger.error(f"Error listing interface addresses: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def list_wildcard_fqdn_addresses(adom: str = "root") -> dict[str, Any]:
    """List wildcard FQDN addresses.
    
    Wildcard FQDN addresses match domain name patterns:
    - *.google.com (all Google subdomains)
    - *.social-media.com (category blocking)
    - mail.*.example.com (regional mail servers)
    
    FortiGate performs DNS resolution and updates the address
    automatically as DNS records change.
    
    Args:
        adom: ADOM name (default: "root")
    
    Returns:
        Dictionary with list of wildcard FQDN addresses
    
    Example:
        result = list_wildcard_fqdn_addresses(adom="root")
    """
    try:
        client = get_fmg_client()
        if not client:
            raise RuntimeError("FortiManager client not initialized")
        
        api = ObjectAPI(client)
        addresses = await api.list_wildcard_fqdn_addresses(adom)
        
        return {
            "status": "success",
            "count": len(addresses),
            "addresses": addresses,
        }
    except Exception as e:
        logger.error(f"Error listing wildcard FQDN addresses: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def list_geography_addresses(adom: str = "root") -> dict[str, Any]:
    """List geography-based addresses.
    
    Geography addresses represent entire countries or regions:
    - Block traffic from high-risk countries
    - Allow only specific geographic regions
    - Implement geo-fencing for compliance
    - GEO-routing based on source location
    
    FortiGate uses FortiGuard IP geolocation database
    which is updated regularly.
    
    Args:
        adom: ADOM name (default: "root")
    
    Returns:
        Dictionary with list of geography addresses
    
    Example:
        result = list_geography_addresses(adom="root")
    """
    try:
        client = get_fmg_client()
        if not client:
            raise RuntimeError("FortiManager client not initialized")
        
        api = ObjectAPI(client)
        addresses = await api.list_geography_addresses(adom)
        
        return {
            "status": "success",
            "count": len(addresses),
            "addresses": addresses,
        }
    except Exception as e:
        logger.error(f"Error listing geography addresses: {e}")
        return {"status": "error", "message": str(e)}


# ============================================================================
# Phase 21: Advanced Objects - Multicast Objects
# ============================================================================


@mcp.tool()
async def list_multicast_addresses(adom: str = "root") -> dict[str, Any]:
    """List multicast addresses.
    
    Multicast addresses are used for group communication:
    - IPTV and video streaming (224.0.0.0/4)
    - Video conferencing
    - Stock trading data feeds
    - Network management protocols (OSPF, PIM)
    
    Multicast policies require both source and multicast group addresses.
    
    Args:
        adom: ADOM name (default: "root")
    
    Returns:
        Dictionary with list of multicast addresses
    
    Example:
        result = list_multicast_addresses(adom="root")
    """
    try:
        client = get_fmg_client()
        if not client:
            raise RuntimeError("FortiManager client not initialized")
        
        api = ObjectAPI(client)
        addresses = await api.list_multicast_addresses(adom)
        
        return {
            "status": "success",
            "count": len(addresses),
            "addresses": addresses,
        }
    except Exception as e:
        logger.error(f"Error listing multicast addresses: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_multicast_address(
    name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Get multicast address details.
    
    Retrieves configuration of a specific multicast address including:
    - Start and end IP (multicast range)
    - Associated interfaces
    - Comments and metadata
    
    Args:
        name: Multicast address name
        adom: ADOM name (default: "root")
    
    Returns:
        Dictionary with multicast address details
    
    Example:
        result = get_multicast_address(
            name="IPTV-Multicast",
            adom="root"
        )
    """
    try:
        client = get_fmg_client()
        if not client:
            raise RuntimeError("FortiManager client not initialized")
        
        api = ObjectAPI(client)
        address = await api.get_multicast_address(name, adom)
        
        return {
            "status": "success",
            "address": address,
        }
    except Exception as e:
        logger.error(f"Error getting multicast address: {e}")
        return {"status": "error", "message": str(e)}


# =============================================================================
# Phase 26: Complete Objects Management
# =============================================================================


@mcp.tool()
async def list_service_categories(adom: str = "root") -> dict[str, Any]:
    """List service categories.
    
    Service categories group related services for easier policy management:
    - Email (SMTP, POP3, IMAP)
    - Web Access (HTTP, HTTPS)
    - Remote Access (SSH, RDP, VNC)
    - File Transfer (FTP, TFTP)
    - VoIP (SIP, H.323)
    
    Categories simplify policy creation by allowing selection of
    service groups instead of individual services.
    
    Args:
        adom: ADOM name (default: "root")
    
    Returns:
        Dictionary with list of service categories
    
    Example:
        result = list_service_categories(adom="root")
    """
    try:
        client = get_fmg_client()
        if not client:
            raise RuntimeError("FortiManager client not initialized")
        
        api = ObjectAPI(client)
        categories = await api.list_service_categories(adom)
        
        return {
            "status": "success",
            "count": len(categories),
            "categories": categories,
        }
    except Exception as e:
        logger.error(f"Error listing service categories: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def list_proxy_addresses(adom: str = "root") -> dict[str, Any]:
    """List proxy addresses for explicit web proxy policies.
    
    Proxy addresses enable granular HTTP/HTTPS control in explicit proxy mode:
    - URL pattern matching (wildcards, regex)
    - Host/domain filtering
    - HTTP method restrictions (GET, POST, etc.)
    - User-agent matching
    - Query string filtering
    
    Used in explicit web proxy policies for precise web filtering beyond
    traditional firewall policies.
    
    Args:
        adom: ADOM name (default: "root")
    
    Returns:
        Dictionary with list of proxy addresses
    
    Example:
        result = list_proxy_addresses(adom="root")
        # Returns proxy addresses for web proxy policies
    """
    try:
        client = get_fmg_client()
        if not client:
            raise RuntimeError("FortiManager client not initialized")
        
        api = ObjectAPI(client)
        addresses = await api.list_proxy_addresses(adom)
        
        return {
            "status": "success",
            "count": len(addresses),
            "addresses": addresses,
        }
    except Exception as e:
        logger.error(f"Error listing proxy addresses: {e}")
        return {"status": "error", "message": str(e)}


# =============================================================================
# Phase 44: Additional Object Operations
# =============================================================================


@mcp.tool()
async def list_ipv6_firewall_addresses(adom: str = "root") -> dict[str, Any]:
    """List IPv6 firewall addresses.
    
    Args:
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with list of IPv6 addresses
    """
    try:
        client = get_fmg_client()
        if not client:
            raise RuntimeError("FortiManager client not initialized")
        
        api = ObjectAPI(client)
        addresses = await api.list_ipv6_addresses(adom)
        
        return {"status": "success", "count": len(addresses), "addresses": addresses}
    except Exception as e:
        logger.error(f"Error listing IPv6 addresses: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def list_ipv6_firewall_address_groups(adom: str = "root") -> dict[str, Any]:
    """List IPv6 address groups.
    
    Args:
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with list of IPv6 address groups
    """
    try:
        client = get_fmg_client()
        if not client:
            raise RuntimeError("FortiManager client not initialized")
        
        api = ObjectAPI(client)
        groups = await api.list_ipv6_address_groups(adom)
        
        return {"status": "success", "count": len(groups), "groups": groups}
    except Exception as e:
        logger.error(f"Error listing IPv6 address groups: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def list_firewall_schedules(adom: str = "root") -> dict[str, Any]:
    """List one-time firewall schedules.
    
    Args:
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with list of schedules
    """
    try:
        client = get_fmg_client()
        if not client:
            raise RuntimeError("FortiManager client not initialized")
        
        api = ObjectAPI(client)
        schedules = await api.list_schedules(adom)
        
        return {"status": "success", "count": len(schedules), "schedules": schedules}
    except Exception as e:
        logger.error(f"Error listing schedules: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def list_firewall_recurring_schedules(adom: str = "root") -> dict[str, Any]:
    """List recurring firewall schedules.
    
    Args:
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with list of recurring schedules
    """
    try:
        client = get_fmg_client()
        if not client:
            raise RuntimeError("FortiManager client not initialized")
        
        api = ObjectAPI(client)
        schedules = await api.list_recurring_schedules(adom)
        
        return {"status": "success", "count": len(schedules), "schedules": schedules}
    except Exception as e:
        logger.error(f"Error listing recurring schedules: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def list_internet_service_definitions(adom: str = "root") -> dict[str, Any]:
    """List custom internet service definitions.
    
    Args:
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with list of internet services
    """
    try:
        client = get_fmg_client()
        if not client:
            raise RuntimeError("FortiManager client not initialized")
        
        api = ObjectAPI(client)
        services = await api.list_internet_services(adom)
        
        return {"status": "success", "count": len(services), "services": services}
    except Exception as e:
        logger.error(f"Error listing internet services: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def list_traffic_shaping_profiles(adom: str = "root") -> dict[str, Any]:
    """List traffic shaping profiles.
    
    Args:
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with list of shaping profiles
    """
    try:
        client = get_fmg_client()
        if not client:
            raise RuntimeError("FortiManager client not initialized")
        
        api = ObjectAPI(client)
        profiles = await api.list_shaping_profiles(adom)
        
        return {"status": "success", "count": len(profiles), "profiles": profiles}
    except Exception as e:
        logger.error(f"Error listing shaping profiles: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def list_firewall_traffic_shapers(adom: str = "root") -> dict[str, Any]:
    """List traffic shapers.
    
    Args:
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with list of traffic shapers
    """
    try:
        client = get_fmg_client()
        if not client:
            raise RuntimeError("FortiManager client not initialized")
        
        api = ObjectAPI(client)
        shapers = await api.list_traffic_shapers(adom)
        
        return {"status": "success", "count": len(shapers), "shapers": shapers}
    except Exception as e:
        logger.error(f"Error listing traffic shapers: {e}")
        return {"status": "error", "message": str(e)}


# =============================================================================
# Phase 48: Advanced Object Types
# =============================================================================


@mcp.tool()
async def list_internet_service_fqdns(adom: str = "root") -> dict[str, Any]:
    """List Internet Service FQDN definitions.
    
    Internet Service FQDNs allow matching cloud/SaaS traffic based on
    fully qualified domain names. Used for:
    - Cloud application identification (Office 365, Google Workspace)
    - SaaS service control
    - Dynamic service matching
    - Application-based policies
    
    These definitions associate FQDNs with FortiGuard Internet Service IDs
    for automatic traffic classification.
    
    Args:
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with list of Internet Service FQDN definitions
    
    Example:
        result = list_internet_service_fqdns(adom="root")
    """
    try:
        client = get_fmg_client()
        if not client:
            raise RuntimeError("FortiManager client not initialized")
        
        api = ObjectAPI(client)
        fqdns = await api.list_internet_service_fqdns(adom)
        
        return {"status": "success", "count": len(fqdns), "fqdns": fqdns}
    except Exception as e:
        logger.error(f"Error listing internet service FQDNs: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def create_internet_service_fqdn(
    name: str,
    internet_service_id: int,
    adom: str = "root",
) -> dict[str, Any]:
    """Create Internet Service FQDN definition.
    
    Associates an FQDN pattern with a FortiGuard Internet Service ID for
    dynamic traffic classification. Useful for:
    - Custom cloud service definitions
    - SaaS application policies
    - Dynamic FQDN-based routing
    
    Args:
        name: Unique name for the FQDN definition
        internet_service_id: FortiGuard Internet Service ID
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with creation result
    
    Example:
        result = create_internet_service_fqdn(
            name="office365-exchange",
            internet_service_id=65536,
            adom="root"
        )
    """
    try:
        client = get_fmg_client()
        if not client:
            raise RuntimeError("FortiManager client not initialized")
        
        api = ObjectAPI(client)
        result = await api.create_internet_service_fqdn(
            name=name,
            internet_service_id=internet_service_id,
            adom=adom,
        )
        
        return {"status": "success", "fqdn": result}
    except Exception as e:
        logger.error(f"Error creating internet service FQDN: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def delete_internet_service_fqdn(
    name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Delete Internet Service FQDN definition.
    
    Removes an Internet Service FQDN definition. Ensure it's not
    referenced in any policies before deletion.
    
    Args:
        name: Name of the FQDN definition to delete
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with deletion result
    
    Example:
        result = delete_internet_service_fqdn(
            name="old-service-fqdn",
            adom="root"
        )
    """
    try:
        client = get_fmg_client()
        if not client:
            raise RuntimeError("FortiManager client not initialized")
        
        api = ObjectAPI(client)
        result = await api.delete_internet_service_fqdn(name, adom)
        
        return {"status": "success", "result": result}
    except Exception as e:
        logger.error(f"Error deleting internet service FQDN: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_normalized_interface_mappings(adom: str = "root") -> dict[str, Any]:
    """Get normalized interface mappings for multi-platform deployments.
    
    Retrieves platform-specific interface name mappings to normalized names.
    Essential for:
    - Multi-platform policy deployment
    - Interface abstraction across device models
    - Cross-device policy consistency
    - Simplified policy management
    
    Normalized interfaces allow policies to reference generic names (e.g.,
    "wan1", "lan1") that automatically map to actual physical interfaces
    on different FortiGate models.
    
    Args:
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with interface mappings
    
    Example:
        result = get_normalized_interface_mappings(adom="root")
        # Returns mappings like: wan1 -> port1 (FG-60F), port5 (FG-100F)
    """
    try:
        client = get_fmg_client()
        if not client:
            raise RuntimeError("FortiManager client not initialized")
        
        api = ObjectAPI(client)
        mappings = await api.get_normalized_interface_mappings(adom)
        
        return {"status": "success", "count": len(mappings), "mappings": mappings}
    except Exception as e:
        logger.error(f"Error getting normalized interface mappings: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def list_replacement_message_groups(adom: str = "root") -> dict[str, Any]:
    """List replacement message groups for custom user notifications.
    
    Replacement message groups customize the messages displayed to users when:
    - Traffic is blocked by policies
    - Content is filtered (web filter, DLP)
    - Authentication is required
    - Virus/malware is detected
    - Disclaimer acceptance needed
    
    Allows branding and customization of all user-facing messages including:
    - HTTP/HTTPS block pages
    - Authentication portals
    - Virus notification pages
    - Custom disclaimers
    
    Args:
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with list of replacement message groups
    
    Example:
        result = list_replacement_message_groups(adom="root")
    """
    try:
        client = get_fmg_client()
        if not client:
            raise RuntimeError("FortiManager client not initialized")
        
        api = ObjectAPI(client)
        groups = await api.list_replacement_message_groups(adom)
        
        return {"status": "success", "count": len(groups), "groups": groups}
    except Exception as e:
        logger.error(f"Error listing replacement message groups: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def list_virtual_wire_pairs(adom: str = "root") -> dict[str, Any]:
    """List virtual wire pair configurations for transparent deployments.
    
    Virtual wire pairs create transparent layer-2 connections between two
    interfaces without requiring IP addresses. Used for:
    - Inline security inspection without network changes
    - Transparent firewall deployment
    - IPS/IDS in transparent mode
    - Traffic monitoring and analysis
    - Tap mode deployments
    
    Virtual wire pairs pass traffic between interfaces transparently while
    applying security policies, perfect for existing networks where routing
    changes are not possible or desired.
    
    Args:
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with list of virtual wire pair configurations
    
    Example:
        result = list_virtual_wire_pairs(adom="root")
        # Returns pairs like: port1 <-> port2 (transparent)
    """
    try:
        client = get_fmg_client()
        if not client:
            raise RuntimeError("FortiManager client not initialized")
        
        api = ObjectAPI(client)
        pairs = await api.list_virtual_wire_pairs(adom)
        
        return {"status": "success", "count": len(pairs), "pairs": pairs}
    except Exception as e:
        logger.error(f"Error listing virtual wire pairs: {e}")
        return {"status": "error", "message": str(e)}

