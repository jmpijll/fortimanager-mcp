"""ADOM Management MCP Tools."""

import logging
from typing import Any

from fortimanager_mcp.api.adoms import ADOMAPI
from fortimanager_mcp.server import get_fmg_client, mcp

logger = logging.getLogger(__name__)


# ============================================================================
# Phase 17: ADOM Management Tools
# ============================================================================


@mcp.tool()
async def clone_adom(
    source_adom: str,
    target_adom: str,
    description: str | None = None,
) -> dict[str, Any]:
    """Clone an ADOM with all its configurations.

    Creates a complete copy of an existing ADOM including all policies, objects,
    and configurations. This is useful for testing changes in a copy before
    applying them to production.

    Args:
        source_adom: Source ADOM name to clone from
        target_adom: Target ADOM name to create
        description: Optional description for the new ADOM

    Returns:
        Dictionary with cloned ADOM details

    Example:
        result = clone_adom(
            source_adom="production",
            target_adom="staging",
            description="Staging environment for testing"
        )
    """
    try:
        client = get_fmg_client()
        if not client:
            raise RuntimeError("FortiManager client not initialized")

        api = ADOMAPI(client)
        adom = await api.clone_adom(
            source_adom=source_adom,
            target_adom=target_adom,
            description=description,
        )

        return {
            "status": "success",
            "adom": {
                "name": adom.name,
                "description": adom.desc,
                "os_version": adom.os_ver,
                "maintenance_release": adom.mr,
            },
            "message": f"ADOM '{target_adom}' cloned from '{source_adom}'",
        }
    except Exception as e:
        logger.error(f"Error cloning ADOM: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def move_device_to_adom(
    device_name: str,
    target_adom: str,
    source_adom: str = "root",
) -> dict[str, Any]:
    """Move a device from one ADOM to another.

    Transfers device management from the source ADOM to the target ADOM.
    This operation updates the device's administrative domain assignment.

    Args:
        device_name: Device name to move
        target_adom: Target ADOM name
        source_adom: Source ADOM name (default: "root")

    Returns:
        Dictionary with operation status

    Example:
        result = move_device_to_adom(
            device_name="FGT-Branch-01",
            target_adom="branch_office",
            source_adom="root"
        )
    """
    try:
        client = get_fmg_client()
        if not client:
            raise RuntimeError("FortiManager client not initialized")

        api = ADOMAPI(client)
        await api.move_device_to_adom(
            device_name=device_name,
            target_adom=target_adom,
            source_adom=source_adom,
        )

        return {
            "status": "success",
            "message": f"Device '{device_name}' moved from '{source_adom}' to '{target_adom}'",
        }
    except Exception as e:
        logger.error(f"Error moving device to ADOM: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def move_vdom_to_adom(
    device_name: str,
    vdom_name: str,
    target_adom: str,
    source_adom: str = "root",
) -> dict[str, Any]:
    """Move a VDOM from one ADOM to another.

    Transfers a specific Virtual Domain from the source ADOM to the target ADOM.
    This allows granular control over which VDOMs are managed by which ADOMs.

    Args:
        device_name: Device name containing the VDOM
        vdom_name: VDOM name to move
        target_adom: Target ADOM name
        source_adom: Source ADOM name (default: "root")

    Returns:
        Dictionary with operation status

    Example:
        result = move_vdom_to_adom(
            device_name="FGT-HQ-01",
            vdom_name="vdom-sales",
            target_adom="sales_adom",
            source_adom="root"
        )
    """
    try:
        client = get_fmg_client()
        if not client:
            raise RuntimeError("FortiManager client not initialized")

        api = ADOMAPI(client)
        await api.move_vdom_to_adom(
            device_name=device_name,
            vdom_name=vdom_name,
            target_adom=target_adom,
            source_adom=source_adom,
        )

        return {
            "status": "success",
            "message": f"VDOM '{vdom_name}' on device '{device_name}' moved from '{source_adom}' to '{target_adom}'",
        }
    except Exception as e:
        logger.error(f"Error moving VDOM to ADOM: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_adom_revision_list(adom: str) -> dict[str, Any]:
    """Get ADOM revision history.

    Retrieves the list of configuration revisions/checkpoints for an ADOM.
    Revisions allow rollback to previous configurations.

    Args:
        adom: ADOM name

    Returns:
        Dictionary with list of revisions

    Example:
        result = get_adom_revision_list(adom="production")
    """
    try:
        client = get_fmg_client()
        if not client:
            raise RuntimeError("FortiManager client not initialized")

        api = ADOMAPI(client)
        revisions = await api.get_adom_revision_list(adom=adom)

        return {
            "status": "success",
            "adom": adom,
            "count": len(revisions),
            "revisions": revisions,
        }
    except Exception as e:
        logger.error(f"Error getting ADOM revision list: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def create_adom_revision(
    adom: str,
    name: str,
    description: str | None = None,
    locked: bool = False,
) -> dict[str, Any]:
    """Create a manual ADOM revision/checkpoint.

    Creates a configuration checkpoint that can be used for rollback.
    This is useful before making significant changes to the ADOM configuration.

    Args:
        adom: ADOM name
        name: Revision name
        description: Optional revision description
        locked: Lock revision to prevent auto-deletion (default: False)

    Returns:
        Dictionary with created revision information

    Example:
        result = create_adom_revision(
            adom="production",
            name="pre-policy-update",
            description="Checkpoint before Q4 policy updates",
            locked=True
        )
    """
    try:
        client = get_fmg_client()
        if not client:
            raise RuntimeError("FortiManager client not initialized")

        api = ADOMAPI(client)
        revision = await api.create_adom_revision(
            adom=adom,
            name=name,
            description=description,
            locked=locked,
        )

        return {
            "status": "success",
            "revision": revision,
            "message": f"Revision '{name}' created for ADOM '{adom}'",
        }
    except Exception as e:
        logger.error(f"Error creating ADOM revision: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def revert_adom_revision(
    adom: str,
    revision_id: int,
) -> dict[str, Any]:
    """Revert ADOM to a specific revision.

    Rolls back the ADOM configuration to a previously saved revision.
    This operation restores all policies, objects, and settings from the specified revision.

    ⚠️  WARNING: This operation cannot be undone. Create a current revision checkpoint first.

    Args:
        adom: ADOM name
        revision_id: Revision ID to revert to

    Returns:
        Dictionary with operation status

    Example:
        # First, create a checkpoint of current state
        create_adom_revision(adom="production", name="before-revert", locked=True)
        
        # Then revert to previous revision
        result = revert_adom_revision(adom="production", revision_id=123)
    """
    try:
        client = get_fmg_client()
        if not client:
            raise RuntimeError("FortiManager client not initialized")

        api = ADOMAPI(client)
        await api.revert_adom_revision(
            adom=adom,
            revision_id=revision_id,
        )

        return {
            "status": "success",
            "message": f"ADOM '{adom}' reverted to revision {revision_id}",
        }
    except Exception as e:
        logger.error(f"Error reverting ADOM revision: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def delete_adom_revision(
    adom: str,
    revision_id: int,
) -> dict[str, Any]:
    """Delete an ADOM revision.

    Removes a specific revision from the ADOM's revision history.
    Locked revisions cannot be deleted and must be unlocked first.

    Args:
        adom: ADOM name
        revision_id: Revision ID to delete

    Returns:
        Dictionary with operation status

    Example:
        result = delete_adom_revision(adom="staging", revision_id=456)
    """
    try:
        client = get_fmg_client()
        if not client:
            raise RuntimeError("FortiManager client not initialized")

        api = ADOMAPI(client)
        await api.delete_adom_revision(
            adom=adom,
            revision_id=revision_id,
        )

        return {
            "status": "success",
            "message": f"Revision {revision_id} deleted from ADOM '{adom}'",
        }
    except Exception as e:
        logger.error(f"Error deleting ADOM revision: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_adom_checksum(adom: str) -> dict[str, Any]:
    """Get ADOM configuration checksum.

    Retrieves the checksum/hash of the ADOM configuration. This is useful for
    verifying configuration integrity and detecting changes.

    Args:
        adom: ADOM name

    Returns:
        Dictionary with checksum information

    Example:
        result = get_adom_checksum(adom="production")
    """
    try:
        client = get_fmg_client()
        if not client:
            raise RuntimeError("FortiManager client not initialized")

        api = ADOMAPI(client)
        checksum = await api.get_adom_checksum(adom=adom)

        return {
            "status": "success",
            "adom": adom,
            "checksum": checksum,
        }
    except Exception as e:
        logger.error(f"Error getting ADOM checksum: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def check_adom_integrity(adom: str) -> dict[str, Any]:
    """Check ADOM database integrity.

    Performs an integrity check on the ADOM database to detect any
    corruption or inconsistencies. This is useful for troubleshooting
    and ensuring database health.

    Args:
        adom: ADOM name

    Returns:
        Dictionary with integrity check results

    Example:
        result = check_adom_integrity(adom="production")
    """
    try:
        client = get_fmg_client()
        if not client:
            raise RuntimeError("FortiManager client not initialized")

        api = ADOMAPI(client)
        result = await api.check_adom_integrity(adom=adom)

        return {
            "status": "success",
            "adom": adom,
            "integrity_check": result,
        }
    except Exception as e:
        logger.error(f"Error checking ADOM integrity: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def upgrade_adom(
    adom: str,
    target_version: str,
    target_mr: int = 0,
) -> dict[str, Any]:
    """Upgrade ADOM to a different FortiOS version.

    Upgrades the ADOM's FortiOS version and maintenance release. This operation
    updates the ADOM database schema and configurations to match the target version.

    ⚠️  WARNING: Create a revision checkpoint before upgrading. Test in a non-production ADOM first.

    Args:
        adom: ADOM name
        target_version: Target FortiOS version (e.g., "7.2", "7.4")
        target_mr: Target maintenance release number (default: 0)

    Returns:
        Dictionary with upgrade task information

    Example:
        # Create checkpoint before upgrade
        create_adom_revision(adom="staging", name="pre-upgrade-7.4", locked=True)
        
        # Perform upgrade
        result = upgrade_adom(
            adom="staging",
            target_version="7.4",
            target_mr=1
        )
    """
    try:
        client = get_fmg_client()
        if not client:
            raise RuntimeError("FortiManager client not initialized")

        api = ADOMAPI(client)
        task = await api.upgrade_adom(
            adom=adom,
            target_version=target_version,
            target_mr=target_mr,
        )

        return {
            "status": "success",
            "adom": adom,
            "target_version": target_version,
            "target_mr": target_mr,
            "task": task,
            "message": f"ADOM upgrade initiated to {target_version} MR{target_mr}",
        }
    except Exception as e:
        logger.error(f"Error upgrading ADOM: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_adom_where_used(
    adom: str,
    object_type: str,
    object_name: str,
) -> dict[str, Any]:
    """Get where an object is used within an ADOM.

    Searches for all references to a specific object within the ADOM.
    This is useful before deleting or modifying objects to understand
    their impact and dependencies.

    Args:
        adom: ADOM name
        object_type: Object type (e.g., "firewall address", "firewall service", "firewall addrgrp")
        object_name: Object name to search for

    Returns:
        Dictionary with list of locations where object is used

    Example:
        result = get_adom_where_used(
            adom="production",
            object_type="firewall address",
            object_name="Corporate-Network"
        )
    """
    try:
        client = get_fmg_client()
        if not client:
            raise RuntimeError("FortiManager client not initialized")

        api = ADOMAPI(client)
        usage = await api.get_adom_where_used(
            adom=adom,
            object_type=object_type,
            object_name=object_name,
        )

        return {
            "status": "success",
            "adom": adom,
            "object_type": object_type,
            "object_name": object_name,
            "usage_count": len(usage),
            "usage_locations": usage,
        }
    except Exception as e:
        logger.error(f"Error getting ADOM object where-used: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_adom_object_usage(adom: str) -> dict[str, Any]:
    """Get ADOM object usage statistics.

    Retrieves statistics about object usage within the ADOM, including
    counts of different object types and their utilization.

    Args:
        adom: ADOM name

    Returns:
        Dictionary with object usage statistics

    Example:
        result = get_adom_object_usage(adom="production")
    """
    try:
        client = get_fmg_client()
        if not client:
            raise RuntimeError("FortiManager client not initialized")

        api = ADOMAPI(client)
        usage = await api.get_adom_object_usage(adom=adom)

        return {
            "status": "success",
            "adom": adom,
            "object_usage": usage,
        }
    except Exception as e:
        logger.error(f"Error getting ADOM object usage: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def assign_device_to_adom(
    device_name: str,
    adom: str,
    vdom: str = "root",
) -> dict[str, Any]:
    """Assign a device/VDOM to an ADOM.

    Associates a specific device and VDOM with an ADOM for management.
    This is typically done during initial device setup or reorganization.

    Args:
        device_name: Device name
        adom: Target ADOM name
        vdom: VDOM name (default: "root")

    Returns:
        Dictionary with operation status

    Example:
        result = assign_device_to_adom(
            device_name="FGT-Branch-05",
            adom="branch_adom",
            vdom="root"
        )
    """
    try:
        client = get_fmg_client()
        if not client:
            raise RuntimeError("FortiManager client not initialized")

        api = ADOMAPI(client)
        await api.assign_device_to_adom(
            device_name=device_name,
            adom=adom,
            vdom=vdom,
        )

        return {
            "status": "success",
            "message": f"Device '{device_name}' VDOM '{vdom}' assigned to ADOM '{adom}'",
        }
    except Exception as e:
        logger.error(f"Error assigning device to ADOM: {e}")
        return {"status": "error", "message": str(e)}


# ============================================================================
# Phase 28: Complete ADOM Management
# ============================================================================


@mcp.tool()
async def lock_adom_workspace(adom: str) -> dict[str, Any]:
    """Lock ADOM workspace for exclusive editing.

    Prevents other administrators from making concurrent changes to the ADOM.
    This is essential when making coordinated configuration changes that
    must be completed atomically.

    The lock must be released with unlock_adom_workspace when done.

    Args:
        adom: ADOM name to lock

    Returns:
        Dictionary with lock status

    Example:
        result = lock_adom_workspace(adom="production")
        # Make changes...
        # Then unlock when done
    """
    try:
        client = get_fmg_client()
        if not client:
            raise RuntimeError("FortiManager client not initialized")

        api = ADOMAPI(client)
        lock_result = await api.lock_adom(adom=adom)

        return {
            "status": "success",
            "message": f"ADOM '{adom}' workspace locked",
            "lock_info": lock_result,
        }
    except Exception as e:
        logger.error(f"Error locking ADOM workspace: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def unlock_adom_workspace(adom: str) -> dict[str, Any]:
    """Unlock ADOM workspace.

    Releases the workspace lock to allow other administrators to make changes.
    Always unlock after completing your changes to prevent blocking others.

    Args:
        adom: ADOM name to unlock

    Returns:
        Dictionary with unlock status

    Example:
        result = unlock_adom_workspace(adom="production")
    """
    try:
        client = get_fmg_client()
        if not client:
            raise RuntimeError("FortiManager client not initialized")

        api = ADOMAPI(client)
        unlock_result = await api.unlock_adom(adom=adom)

        return {
            "status": "success",
            "message": f"ADOM '{adom}' workspace unlocked",
            "unlock_info": unlock_result,
        }
    except Exception as e:
        logger.error(f"Error unlocking ADOM workspace: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_adom_policy_sync_status(adom: str) -> dict[str, Any]:
    """Get ADOM policy synchronization status.

    Shows whether policies in the ADOM database are synchronized with
    managed devices. Useful for identifying devices with outdated policies.

    Args:
        adom: ADOM name

    Returns:
        Dictionary with policy sync status

    Example:
        result = get_adom_policy_sync_status(adom="production")
        # Returns sync status for all devices in ADOM
    """
    try:
        client = get_fmg_client()
        if not client:
            raise RuntimeError("FortiManager client not initialized")

        api = ADOMAPI(client)
        sync_status = await api.get_adom_policy_sync_status(adom=adom)

        return {
            "status": "success",
            "adom": adom,
            "sync_status": sync_status,
        }
    except Exception as e:
        logger.error(f"Error getting ADOM policy sync status: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_adom_metadata_fields(adom: str) -> dict[str, Any]:
    """Get ADOM metadata fields and values.

    Retrieves custom metadata (key-value pairs) associated with an ADOM.
    Metadata is used for:
    - Categorization (e.g., "environment"="production")
    - Compliance tracking
    - Automation tagging
    - Custom reporting

    Args:
        adom: ADOM name

    Returns:
        Dictionary with list of metadata fields

    Example:
        result = get_adom_metadata_fields(adom="production")
        # Returns all custom metadata tags
    """
    try:
        client = get_fmg_client()
        if not client:
            raise RuntimeError("FortiManager client not initialized")

        api = ADOMAPI(client)
        meta_fields = await api.get_adom_meta_fields(adom=adom)

        return {
            "status": "success",
            "adom": adom,
            "count": len(meta_fields),
            "metadata": meta_fields,
        }
    except Exception as e:
        logger.error(f"Error getting ADOM metadata fields: {e}")
        return {"status": "error", "message": str(e)}


# ============================================================================
# Phase 43: Complete ADOM Operations
# ============================================================================


@mcp.tool()
async def get_adom_statistics(adom: str = "root") -> dict[str, Any]:
    """Get comprehensive statistics for an ADOM including devices, policies, and objects count."""
    try:
        client = get_fmg_client()
        if not client:
            raise RuntimeError("FortiManager client not initialized")
        api = ADOMAPI(client)
        stats = await api.get_adom_statistics(adom=adom)
        return {"status": "success", "adom": adom, "statistics": stats}
    except Exception as e:
        logger.error(f"Error getting ADOM statistics: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def export_adom_config(adom: str = "root") -> dict[str, Any]:
    """Export ADOM configuration for backup purposes."""
    try:
        client = get_fmg_client()
        if not client:
            raise RuntimeError("FortiManager client not initialized")
        api = ADOMAPI(client)
        config = await api.export_adom_configuration(adom=adom)
        return {"status": "success", "adom": adom, "configuration": config}
    except Exception as e:
        logger.error(f"Error exporting ADOM configuration: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_adom_health(adom: str = "root") -> dict[str, Any]:
    """Get health status of ADOM including all managed devices."""
    try:
        client = get_fmg_client()
        if not client:
            raise RuntimeError("FortiManager client not initialized")
        api = ADOMAPI(client)
        health = await api.get_adom_health_status(adom=adom)
        return {"status": "success", "adom": adom, "health": health}
    except Exception as e:
        logger.error(f"Error getting ADOM health: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_adom_disk_usage(adom: str = "root") -> dict[str, Any]:
    """Get disk usage statistics for ADOM data storage."""
    try:
        client = get_fmg_client()
        if not client:
            raise RuntimeError("FortiManager client not initialized")
        api = ADOMAPI(client)
        usage = await api.get_adom_disk_usage(adom=adom)
        return {"status": "success", "adom": adom, "disk_usage": usage}
    except Exception as e:
        logger.error(f"Error getting ADOM disk usage: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def list_adom_templates(adom: str = "root") -> dict[str, Any]:
    """List all CLI templates configured in an ADOM."""
    try:
        client = get_fmg_client()
        if not client:
            raise RuntimeError("FortiManager client not initialized")
        api = ADOMAPI(client)
        templates = await api.list_adom_templates(adom=adom)
        return {"status": "success", "adom": adom, "count": len(templates), "templates": templates}
    except Exception as e:
        logger.error(f"Error listing ADOM templates: {e}")
        return {"status": "error", "message": str(e)}


# =============================================================================
# Phase 45: Final Operations to 100%
# =============================================================================


@mcp.tool()
async def get_adom_object_statistics(adom: str = "root") -> dict[str, Any]:
    """Get comprehensive object count statistics for an ADOM.
    
    Provides counts of all object types including addresses, services,
    groups, profiles, and other configuration objects.
    
    Args:
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with object count statistics
    """
    try:
        api = _get_adom_api()
        stats = await api.get_adom_object_count(adom=adom)
        return {"status": "success", "adom": adom, "object_counts": stats}
    except Exception as e:
        logger.error(f"Error getting ADOM object statistics: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_adom_policy_statistics(adom: str = "root") -> dict[str, Any]:
    """Get comprehensive policy count statistics for an ADOM.
    
    Provides counts of all policies across all packages in the ADOM.
    
    Args:
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with policy count statistics
    """
    try:
        api = _get_adom_api()
        stats = await api.get_adom_policy_count(adom=adom)
        return {"status": "success", "adom": adom, "policy_counts": stats}
    except Exception as e:
        logger.error(f"Error getting ADOM policy statistics: {e}")
        return {"status": "error", "message": str(e)}


# =============================================================================
# Phase 46: ADOM Advanced Operations
# =============================================================================


@mcp.tool()
async def create_advanced_adom(
    name: str,
    os_version: str,
    description: str = "",
    maintenance_release: int = 0,
    enable_central_management: bool = True,
    enable_split_task: bool = True,
    restricted_products: str | None = None,
) -> dict[str, Any]:
    """Create ADOM with advanced configuration options.
    
    Provides fine-grained control over ADOM creation including OS version,
    maintenance release, management flags, and product restrictions.
    
    This is useful for creating ADOMs with specific FortiOS version requirements
    or with specialized management settings.
    
    Args:
        name: ADOM name (must be unique)
        os_version: FortiOS version - "6.0", "7.0", "7.2", "7.4"
        description: Human-readable description
        maintenance_release: MR number (e.g., 13 for 7.0.13, 8 for 7.4.8)
        enable_central_management: Enable central management features
        enable_split_task: Enable split task processing for performance
        restricted_products: Comma-separated product codes (e.g., "fos,fml")
    
    Returns:
        Dictionary with creation status and ADOM details
    
    Example:
        result = create_advanced_adom(
            name="prod-fos74",
            os_version="7.4",
            maintenance_release=8,
            description="Production ADOM for FortiOS 7.4.8 devices",
            restricted_products="fos"
        )
    """
    try:
        api = _get_adom_api()
        
        # Parse restricted products if provided
        products_list = None
        if restricted_products:
            products_list = [p.strip() for p in restricted_products.split(",")]
        
        result = await api.create_adom_advanced(
            name=name,
            os_version=os_version,
            description=description,
            maintenance_release=maintenance_release,
            enable_central_management=enable_central_management,
            enable_split_task=enable_split_task,
            restricted_products=products_list,
        )
        
        return {
            "status": "success",
            "message": f"ADOM '{name}' created with advanced configuration",
            "adom": result,
        }
    except Exception as e:
        logger.error(f"Error creating advanced ADOM: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def create_adom_with_device_assignment(
    name: str,
    os_version: str,
    device_assignments: str,
    description: str = "",
) -> dict[str, Any]:
    """Create ADOM and assign devices in one atomic operation.
    
    Creates a new ADOM and immediately assigns specified devices to it.
    This is more efficient than creating the ADOM and moving devices separately.
    
    Args:
        name: ADOM name (must be unique)
        os_version: FortiOS version - "6.0", "7.0", "7.2", "7.4"
        device_assignments: JSON string or comma-separated list of devices
            Format: "device1:vdom1,device2:vdom2" or JSON array
        description: ADOM description
    
    Returns:
        Dictionary with creation status
    
    Example:
        result = create_adom_with_device_assignment(
            name="branch-offices",
            os_version="7.2",
            device_assignments="FGT-BRANCH-01:root,FGT-BRANCH-02:root",
            description="Branch office devices"
        )
    """
    try:
        api = _get_adom_api()
        
        # Parse device assignments
        devices = []
        if device_assignments.strip().startswith("["):
            # JSON format
            import json
            devices = json.loads(device_assignments)
        else:
            # Comma-separated format: "device1:vdom1,device2:vdom2"
            for assignment in device_assignments.split(","):
                parts = assignment.strip().split(":")
                if len(parts) == 2:
                    devices.append({"name": parts[0].strip(), "vdom": parts[1].strip()})
                else:
                    devices.append({"name": parts[0].strip(), "vdom": "root"})
        
        result = await api.create_adom_with_devices(
            name=name,
            os_version=os_version,
            devices=devices,
            description=description,
        )
        
        return {
            "status": "success",
            "message": f"ADOM '{name}' created with {len(devices)} device(s) assigned",
            "adom": result,
            "devices_assigned": len(devices),
        }
    except Exception as e:
        logger.error(f"Error creating ADOM with device assignment: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_adom_display_settings() -> dict[str, Any]:
    """Get ADOM display and selection preferences from FortiManager.
    
    Retrieves system-level settings that control how ADOMs are displayed
    and selected in the FortiManager interface and API operations.
    
    Returns:
        Dictionary with ADOM display configuration
    
    Example:
        result = get_adom_display_settings()
        # Returns: {adom_enabled: true, adom_select_mode: "auto", ...}
    """
    try:
        api = _get_adom_api()
        settings = await api.get_adom_display_preferences()
        
        return {
            "status": "success",
            "settings": settings,
        }
    except Exception as e:
        logger.error(f"Error getting ADOM display settings: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_adom_limits(adom: str = "root") -> dict[str, Any]:
    """Get ADOM resource limits and current usage.
    
    Retrieves capacity limits and current resource utilization for an ADOM.
    Useful for capacity planning, monitoring resource usage, and understanding
    the maximum scale of objects, policies, and devices in the ADOM.
    
    Args:
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with resource limits and usage
    
    Example:
        result = get_adom_limits(adom="production")
        # Returns max and current counts for devices, policies, objects
    """
    try:
        api = _get_adom_api()
        limits = await api.get_adom_resource_limits(adom=adom)
        
        return {
            "status": "success",
            "adom": adom,
            "limits": limits,
        }
    except Exception as e:
        logger.error(f"Error getting ADOM resource limits: {e}")
        return {"status": "error", "message": str(e)}


