"""Meta Fields MCP Tools."""

import logging
from typing import Any

from fortimanager_mcp.api.metafields import MetaFieldsAPI
from fortimanager_mcp.server import get_fmg_client, mcp

logger = logging.getLogger(__name__)


def _get_metafields_api() -> MetaFieldsAPI:
    client = get_fmg_client()
    if not client:
        raise RuntimeError("FortiManager client not initialized")
    return MetaFieldsAPI(client)


# =============================================================================
# Phase 32: Meta Fields
# =============================================================================


@mcp.tool()
async def list_meta_fields(adom: str = "root") -> dict[str, Any]:
    """List all meta field definitions.
    
    Meta fields enable custom categorization and tagging of FortiManager objects:
    - **Policy metadata**: Business owner, compliance tags, change tickets
    - **Object metadata**: Environment (prod/test), criticality, cost center
    - **Device metadata**: Location, maintenance window, support tier
    
    Use cases:
    - Compliance reporting and auditing
    - Automation workflows and orchestration
    - Custom dashboards and analytics
    - Change management tracking
    
    Args:
        adom: ADOM name (default: "root")
    
    Returns:
        Dictionary with list of meta field definitions
    
    Example:
        result = list_meta_fields(adom="root")
    """
    try:
        api = _get_metafields_api()
        fields = await api.list_meta_fields(adom=adom)
        return {
            "status": "success",
            "count": len(fields),
            "meta_fields": fields,
        }
    except Exception as e:
        logger.error(f"Error listing meta fields: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_meta_field(name: str, adom: str = "root") -> dict[str, Any]:
    """Get meta field definition and properties.
    
    Retrieves complete definition including:
    - Field type (string, integer, boolean)
    - Valid values/options
    - Default value
    - Description
    
    Args:
        name: Meta field name
        adom: ADOM name (default: "root")
    
    Returns:
        Dictionary with meta field definition
    
    Example:
        result = get_meta_field(name="environment", adom="root")
    """
    try:
        api = _get_metafields_api()
        field = await api.get_meta_field(name=name, adom=adom)
        return {
            "status": "success",
            "meta_field": field,
        }
    except Exception as e:
        logger.error(f"Error getting meta field: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def create_meta_field(
    name: str,
    field_type: str = "string",
    adom: str = "root",
) -> dict[str, Any]:
    """Create a new meta field definition.
    
    Defines a custom metadata field that can be assigned to objects.
    
    Args:
        name: Meta field name (e.g., "environment", "cost_center")
        field_type: Field type - "string", "integer", or "boolean"
        adom: ADOM name (default: "root")
    
    Returns:
        Dictionary with created meta field
    
    Example:
        result = create_meta_field(
            name="business_unit",
            field_type="string",
            adom="root"
        )
    """
    try:
        api = _get_metafields_api()
        field = await api.create_meta_field(
            name=name,
            field_type=field_type,
            adom=adom,
        )
        return {
            "status": "success",
            "message": f"Meta field '{name}' created",
            "meta_field": field,
        }
    except Exception as e:
        logger.error(f"Error creating meta field: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def delete_meta_field(name: str, adom: str = "root") -> dict[str, Any]:
    """Delete a meta field definition.
    
    Removes the meta field definition. Existing values on objects
    will be removed.
    
    Args:
        name: Meta field name
        adom: ADOM name (default: "root")
    
    Returns:
        Dictionary with deletion result
    
    Example:
        result = delete_meta_field(name="old_field", adom="root")
    """
    try:
        api = _get_metafields_api()
        result = await api.delete_meta_field(name=name, adom=adom)
        return {
            "status": "success",
            "message": f"Meta field '{name}' deleted",
            "result": result,
        }
    except Exception as e:
        logger.error(f"Error deleting meta field: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def list_objects_with_meta_field(
    field_name: str,
    field_value: str,
    object_type: str = "firewall/address",
    adom: str = "root",
) -> dict[str, Any]:
    """Find all objects with a specific meta field value.
    
    Search for objects by metadata tags:
    - Find all production firewall addresses
    - Locate policies owned by specific team
    - Identify devices in maintenance window
    
    Args:
        field_name: Meta field name to search
        field_value: Meta field value to match
        object_type: Object type (default: "firewall/address")
            - "firewall/address"
            - "firewall/policy"
            - "firewall/service/custom"
        adom: ADOM name (default: "root")
    
    Returns:
        Dictionary with matching objects
    
    Example:
        result = list_objects_with_meta_field(
            field_name="environment",
            field_value="production",
            object_type="firewall/address",
            adom="root"
        )
    """
    try:
        api = _get_metafields_api()
        objects = await api.list_objects_with_meta_field(
            field_name=field_name,
            field_value=field_value,
            object_type=object_type,
            adom=adom,
        )
        return {
            "status": "success",
            "count": len(objects),
            "objects": objects,
        }
    except Exception as e:
        logger.error(f"Error listing objects with meta field: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def set_object_meta_field(
    object_name: str,
    object_type: str,
    field_name: str,
    field_value: Any,
    adom: str = "root",
) -> dict[str, Any]:
    """Set a meta field value on an object.
    
    Tag objects with custom metadata for organization and automation.
    
    Args:
        object_name: Object name
        object_type: Object type (e.g., "firewall/address")
        field_name: Meta field name
        field_value: Meta field value
        adom: ADOM name (default: "root")
    
    Returns:
        Dictionary with operation result
    
    Example:
        result = set_object_meta_field(
            object_name="internal_servers",
            object_type="firewall/address",
            field_name="environment",
            field_value="production",
            adom="root"
        )
    """
    try:
        api = _get_metafields_api()
        await api.set_object_meta_field(
            object_name=object_name,
            object_type=object_type,
            field_name=field_name,
            field_value=field_value,
            adom=adom,
        )
        return {
            "status": "success",
            "message": f"Meta field '{field_name}' set to '{field_value}' on {object_name}",
        }
    except Exception as e:
        logger.error(f"Error setting object meta field: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_object_meta_fields(
    object_name: str,
    object_type: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Get all meta fields for an object.
    
    Retrieves all metadata tags assigned to an object.
    
    Args:
        object_name: Object name
        object_type: Object type (e.g., "firewall/address")
        adom: ADOM name (default: "root")
    
    Returns:
        Dictionary with object's meta fields
    
    Example:
        result = get_object_meta_fields(
            object_name="dmz_servers",
            object_type="firewall/address",
            adom="root"
        )
    """
    try:
        api = _get_metafields_api()
        meta_fields = await api.get_object_meta_fields(
            object_name=object_name,
            object_type=object_type,
            adom=adom,
        )
        return {
            "status": "success",
            "object": object_name,
            "meta_fields": meta_fields,
        }
    except Exception as e:
        logger.error(f"Error getting object meta fields: {e}")
        return {"status": "error", "message": str(e)}

