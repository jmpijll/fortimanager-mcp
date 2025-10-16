"""Sub-Object Fetch MCP Tools."""

import logging
from typing import Any

from fortimanager_mcp.api.subfetch import SubFetchAPI
from fortimanager_mcp.server import get_fmg_client, mcp

logger = logging.getLogger(__name__)


def _get_subfetch_api() -> SubFetchAPI:
    client = get_fmg_client()
    if not client:
        raise RuntimeError("FortiManager client not initialized")
    return SubFetchAPI(client)


# =============================================================================
# Phase 34: Sub-Object Fetch Operations
# =============================================================================


@mcp.tool()
async def fetch_sub_objects(
    object_path: str,
    sub_object_type: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Fetch sub-objects from a parent configuration object.
    
    Retrieves nested configuration objects within a parent object. Useful for:
    - Getting entries within a profile (IPS signatures, web filter rules)
    - Listing members of complex objects
    - Retrieving nested policy elements
    
    Common sub-object types:
    - **entries**: Profile entries (IPS, DLP, web filter)
    - **rule**: Policy-specific rules
    - **member**: Group members
    - **interface**: Interface sub-configurations
    
    Args:
        object_path: Parent object path (e.g., "webfilter/profile/default")
        sub_object_type: Type of sub-object (e.g., "entries")
        adom: ADOM name (default: "root")
    
    Returns:
        Dictionary with list of sub-objects
    
    Example:
        result = fetch_sub_objects(
            object_path="ips/sensor/default",
            sub_object_type="entries",
            adom="root"
        )
    """
    try:
        api = _get_subfetch_api()
        sub_objects = await api.fetch_sub_objects(
            object_path=object_path,
            sub_object_type=sub_object_type,
            adom=adom,
        )
        return {
            "status": "success",
            "count": len(sub_objects),
            "sub_objects": sub_objects,
        }
    except Exception as e:
        logger.error(f"Error fetching sub-objects: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def fetch_nested_configuration(
    config_path: str,
    depth: int = 1,
    adom: str = "root",
) -> dict[str, Any]:
    """Fetch configuration with nested sub-objects.
    
    Retrieves a configuration object including all nested sub-configurations
    up to the specified depth level. This provides a complete view of
    complex hierarchical configurations.
    
    Depth levels:
    - **1**: Immediate children only
    - **2**: Children and grandchildren
    - **3-5**: Deeper nesting levels
    
    Use cases:
    - Export complete policy configuration
    - Backup complex security profiles
    - Analyze nested object relationships
    - Clone configurations with dependencies
    
    Args:
        config_path: Configuration path (e.g., "firewall/policy/default")
        depth: Nesting depth to retrieve (1-5, default: 1)
        adom: ADOM name (default: "root")
    
    Returns:
        Dictionary with nested configuration
    
    Example:
        result = fetch_nested_configuration(
            config_path="firewall/policy/default",
            depth=2,
            adom="root"
        )
    """
    try:
        api = _get_subfetch_api()
        config = await api.fetch_nested_configuration(
            config_path=config_path,
            depth=depth,
            adom=adom,
        )
        return {
            "status": "success",
            "configuration": config,
        }
    except Exception as e:
        logger.error(f"Error fetching nested configuration: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def fetch_object_members(
    object_type: str,
    object_name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Fetch members of a group object.
    
    Retrieves detailed information about all members in a group object:
    - **Address groups**: Individual addresses and ranges
    - **Service groups**: Services and ports
    - **User groups**: Users and external authentication sources
    - **Device groups**: Managed devices
    
    Returns complete member details, not just names, enabling
    full analysis of group composition.
    
    Args:
        object_type: Object type (e.g., "firewall/addrgrp", "firewall/service/group")
        object_name: Group object name
        adom: ADOM name (default: "root")
    
    Returns:
        Dictionary with list of member objects
    
    Example:
        result = fetch_object_members(
            object_type="firewall/addrgrp",
            object_name="internal_networks",
            adom="root"
        )
    """
    try:
        api = _get_subfetch_api()
        members = await api.fetch_object_members(
            object_type=object_type,
            object_name=object_name,
            adom=adom,
        )
        return {
            "status": "success",
            "object": object_name,
            "count": len(members),
            "members": members,
        }
    except Exception as e:
        logger.error(f"Error fetching object members: {e}")
        return {"status": "error", "message": str(e)}


