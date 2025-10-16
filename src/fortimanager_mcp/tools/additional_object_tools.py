"""MCP tools for additional firewall and security objects."""

import logging
from typing import Any

from fortimanager_mcp.api.additional_objects import AdditionalObjectsAPI
from fortimanager_mcp.server import get_fmg_client, mcp

logger = logging.getLogger(__name__)


def _get_additional_objects_api() -> AdditionalObjectsAPI:
    """Get Additional Objects API instance."""
    client = get_fmg_client()
    return AdditionalObjectsAPI(client)


# ============================================================================
# Internet Service Objects
# ============================================================================

@mcp.tool()
async def list_internet_services(adom: str = "root") -> dict[str, Any]:
    """List internet service name objects.
    
    Internet services are predefined FortiGuard objects for popular
    applications like Office365, Dropbox, etc.
    
    Args:
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with internet service names list
    """
    try:
        api = _get_additional_objects_api()
        services = await api.list_internet_service_names(adom=adom)
        return {
            "status": "success",
            "count": len(services),
            "internet_services": services,
        }
    except Exception as e:
        logger.error(f"Error listing internet services in ADOM {adom}: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def list_internet_service_groups(adom: str = "root") -> dict[str, Any]:
    """List internet service groups.
    
    Groups of internet services for convenient use in policies.
    
    Args:
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with internet service groups list
    """
    try:
        api = _get_additional_objects_api()
        groups = await api.list_internet_service_groups(adom=adom)
        return {
            "status": "success",
            "count": len(groups),
            "internet_service_groups": groups,
        }
    except Exception as e:
        logger.error(f"Error listing internet service groups in ADOM {adom}: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def create_internet_service_group(
    name: str,
    members: list[str],
    adom: str = "root",
) -> dict[str, Any]:
    """Create an internet service group.
    
    Args:
        name: Group name
        members: List of internet service names to include
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with creation result
        
    Example:
        result = create_internet_service_group(
            name="cloud-services",
            members=["Office365", "Google-Drive", "Dropbox"],
            adom="production"
        )
    """
    try:
        api = _get_additional_objects_api()
        result = await api.create_internet_service_group(
            name=name,
            members=members,
            adom=adom,
        )
        return {
            "status": "success",
            "message": f"Internet service group '{name}' created with {len(members)} members",
            "result": result,
        }
    except Exception as e:
        logger.error(f"Error creating internet service group '{name}': {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def delete_internet_service_group(name: str, adom: str = "root") -> dict[str, Any]:
    """Delete an internet service group.
    
    Args:
        name: Group name
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with deletion result
    """
    try:
        api = _get_additional_objects_api()
        result = await api.delete_internet_service_group(name=name, adom=adom)
        return {
            "status": "success",
            "message": f"Internet service group '{name}' deleted",
            "result": result,
        }
    except Exception as e:
        logger.error(f"Error deleting internet service group '{name}': {e}")
        return {"status": "error", "message": str(e)}


# ============================================================================
# Security Profile Groups
# ============================================================================

@mcp.tool()
async def list_security_profile_groups(adom: str = "root") -> dict[str, Any]:
    """List security profile groups.
    
    Profile groups bundle multiple security profiles (Antivirus, Web Filter,
    IPS, Application Control, etc.) for easy application to policies.
    
    Args:
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with profile groups list
    """
    try:
        api = _get_additional_objects_api()
        groups = await api.list_profile_groups(adom=adom)
        return {
            "status": "success",
            "count": len(groups),
            "profile_groups": groups,
        }
    except Exception as e:
        logger.error(f"Error listing profile groups in ADOM {adom}: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_security_profile_group(name: str, adom: str = "root") -> dict[str, Any]:
    """Get details of a security profile group.
    
    Args:
        name: Profile group name
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with profile group details
    """
    try:
        api = _get_additional_objects_api()
        group = await api.get_profile_group(name=name, adom=adom)
        return {
            "status": "success",
            "profile_group": group,
        }
    except Exception as e:
        logger.error(f"Error getting profile group '{name}': {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def create_security_profile_group(
    name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Create a security profile group.
    
    Args:
        name: Profile group name
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with creation result
        
    Example:
        # Create a profile group (profiles are assigned via update)
        result = create_security_profile_group(
            name="full-protection",
            adom="production"
        )
    """
    try:
        api = _get_additional_objects_api()
        result = await api.create_profile_group(name=name, adom=adom)
        return {
            "status": "success",
            "message": f"Security profile group '{name}' created",
            "result": result,
        }
    except Exception as e:
        logger.error(f"Error creating profile group '{name}': {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def delete_security_profile_group(name: str, adom: str = "root") -> dict[str, Any]:
    """Delete a security profile group.
    
    Args:
        name: Profile group name
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with deletion result
    """
    try:
        api = _get_additional_objects_api()
        result = await api.delete_profile_group(name=name, adom=adom)
        return {
            "status": "success",
            "message": f"Security profile group '{name}' deleted",
            "result": result,
        }
    except Exception as e:
        logger.error(f"Error deleting profile group '{name}': {e}")
        return {"status": "error", "message": str(e)}


# ============================================================================
# Custom Applications
# ============================================================================

@mcp.tool()
async def list_custom_applications(adom: str = "root") -> dict[str, Any]:
    """List custom application signatures.
    
    Custom applications extend FortiGuard's built-in application control
    with user-defined application signatures.
    
    Args:
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with custom applications list
    """
    try:
        api = _get_additional_objects_api()
        apps = await api.list_custom_applications(adom=adom)
        return {
            "status": "success",
            "count": len(apps),
            "custom_applications": apps,
        }
    except Exception as e:
        logger.error(f"Error listing custom applications in ADOM {adom}: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_custom_application(tag: str, adom: str = "root") -> dict[str, Any]:
    """Get details of a custom application.
    
    Args:
        tag: Application tag/name
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with custom application details
    """
    try:
        api = _get_additional_objects_api()
        app = await api.get_custom_application(tag=tag, adom=adom)
        return {
            "status": "success",
            "custom_application": app,
        }
    except Exception as e:
        logger.error(f"Error getting custom application '{tag}': {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def create_custom_application(
    tag: str,
    protocol: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Create a custom application signature.
    
    Args:
        tag: Application tag/name
        protocol: Protocol ("TCP/UDP", "TCP", or "UDP")
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with creation result
        
    Example:
        result = create_custom_application(
            tag="custom-app-1",
            protocol="TCP",
            adom="production"
        )
    """
    try:
        api = _get_additional_objects_api()
        result = await api.create_custom_application(
            tag=tag,
            protocol=protocol,
            adom=adom,
        )
        return {
            "status": "success",
            "message": f"Custom application '{tag}' created",
            "result": result,
        }
    except Exception as e:
        logger.error(f"Error creating custom application '{tag}': {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def delete_custom_application(tag: str, adom: str = "root") -> dict[str, Any]:
    """Delete a custom application.
    
    Args:
        tag: Application tag/name
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with deletion result
    """
    try:
        api = _get_additional_objects_api()
        result = await api.delete_custom_application(tag=tag, adom=adom)
        return {
            "status": "success",
            "message": f"Custom application '{tag}' deleted",
            "result": result,
        }
    except Exception as e:
        logger.error(f"Error deleting custom application '{tag}': {e}")
        return {"status": "error", "message": str(e)}


# ============================================================================
# DNS Filter Domains
# ============================================================================

@mcp.tool()
async def list_dns_filter_domains(adom: str = "root") -> dict[str, Any]:
    """List DNS filter domain lists.
    
    DNS filter domains are custom blocklists/allowlists for DNS filtering.
    
    Args:
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with DNS filter domains list
    """
    try:
        api = _get_additional_objects_api()
        domains = await api.list_dns_filter_domains(adom=adom)
        return {
            "status": "success",
            "count": len(domains),
            "dns_filter_domains": domains,
        }
    except Exception as e:
        logger.error(f"Error listing DNS filter domains in ADOM {adom}: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_dns_filter_domain(filter_id: int, adom: str = "root") -> dict[str, Any]:
    """Get details of a DNS filter domain list.
    
    Args:
        filter_id: Domain filter ID
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with DNS filter domain details
    """
    try:
        api = _get_additional_objects_api()
        domain = await api.get_dns_filter_domain(id=filter_id, adom=adom)
        return {
            "status": "success",
            "dns_filter_domain": domain,
        }
    except Exception as e:
        logger.error(f"Error getting DNS filter domain {filter_id}: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def create_dns_filter_domain(
    name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Create a DNS filter domain list.
    
    Args:
        name: Domain filter name
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with creation result
        
    Example:
        result = create_dns_filter_domain(
            name="blocked-domains",
            adom="production"
        )
    """
    try:
        api = _get_additional_objects_api()
        result = await api.create_dns_filter_domain(name=name, adom=adom)
        return {
            "status": "success",
            "message": f"DNS filter domain list '{name}' created",
            "result": result,
        }
    except Exception as e:
        logger.error(f"Error creating DNS filter domain '{name}': {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def delete_dns_filter_domain(filter_id: int, adom: str = "root") -> dict[str, Any]:
    """Delete a DNS filter domain list.
    
    Args:
        filter_id: Domain filter ID
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with deletion result
    """
    try:
        api = _get_additional_objects_api()
        result = await api.delete_dns_filter_domain(id=filter_id, adom=adom)
        return {
            "status": "success",
            "message": f"DNS filter domain {filter_id} deleted",
            "result": result,
        }
    except Exception as e:
        logger.error(f"Error deleting DNS filter domain {filter_id}: {e}")
        return {"status": "error", "message": str(e)}

