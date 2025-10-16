"""MCP tools for workspace and FortiManager operations."""

from typing import Any

from fortimanager_mcp.api.workspace import WorkspaceAPI
from fortimanager_mcp.server import get_fmg_client, mcp


def _get_workspace_api() -> WorkspaceAPI:
    """Get Workspace API instance."""
    client = get_fmg_client()
    return WorkspaceAPI(client)


# ============================================================================
# ADOM Workspace Operations
# ============================================================================

@mcp.tool()
async def lock_adom_workspace(adom: str = "root") -> dict[str, Any]:
    """Lock an ADOM workspace for safe editing.
    
    Locking an ADOM prevents other administrators from making changes while
    you work. This is essential for maintaining consistency in multi-admin
    environments.
    
    **Important:** Always unlock or commit when done!
    
    Args:
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with lock operation result
        
    Example:
        # Lock the production ADOM before making changes
        result = lock_adom_workspace(adom="production")
    """
    try:
        api = _get_workspace_api()
        result = await api.lock_adom(adom=adom)
        return {
            "status": "success",
            "message": f"ADOM '{adom}' locked successfully",
            "warning": "Remember to commit or unlock when done!",
            "result": result,
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def unlock_adom_workspace(adom: str = "root") -> dict[str, Any]:
    """Unlock an ADOM workspace.
    
    **WARNING:** Unlocking without committing will discard all unsaved changes!
    Use commit_adom_workspace first to save your changes.
    
    Args:
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with unlock operation result
        
    Example:
        # Unlock after committing changes
        result = unlock_adom_workspace(adom="production")
    """
    try:
        api = _get_workspace_api()
        result = await api.unlock_adom(adom=adom)
        return {
            "status": "success",
            "message": f"ADOM '{adom}' unlocked",
            "warning": "Any uncommitted changes have been discarded",
            "result": result,
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def commit_adom_workspace(adom: str = "root") -> dict[str, Any]:
    """Commit changes to an ADOM workspace.
    
    Saves all pending changes made while the ADOM was locked. This creates
    a new ADOM revision that can be reverted if needed.
    
    The commit operation does NOT unlock the ADOM - you must still unlock
    after committing.
    
    Args:
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with commit operation result
        
    Example:
        # Typical workflow:
        # 1. Lock ADOM
        lock_adom_workspace(adom="production")
        # 2. Make changes
        # 3. Commit changes
        commit_adom_workspace(adom="production")
        # 4. Unlock ADOM
        unlock_adom_workspace(adom="production")
    """
    try:
        api = _get_workspace_api()
        result = await api.commit_adom(adom=adom)
        return {
            "status": "success",
            "message": f"Changes committed to ADOM '{adom}'",
            "note": "A new ADOM revision has been created",
            "reminder": "Don't forget to unlock the ADOM",
            "result": result,
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_adom_lock_status(adom: str = "root") -> dict[str, Any]:
    """Get workspace lock status for an ADOM.
    
    Shows whether the ADOM is locked, who locked it, when, and if there
    are pending changes (dirty flag).
    
    Args:
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with lock information
        
    Example:
        result = get_adom_lock_status(adom="production")
        # Returns info about current lock holder and pending changes
    """
    try:
        api = _get_workspace_api()
        lock_info = await api.get_lock_info(adom=adom)
        return {
            "status": "success",
            "adom": adom,
            "lock_info": lock_info,
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


# ============================================================================
# Policy Package Workspace Operations
# ============================================================================

@mcp.tool()
async def lock_policy_package_workspace(
    package: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Lock a policy package for editing.
    
    Locking a specific package instead of the entire ADOM allows more
    granular control in environments with multiple administrators.
    
    Args:
        package: Policy package name
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with lock operation result
        
    Example:
        result = lock_policy_package_workspace(
            package="default",
            adom="production"
        )
    """
    try:
        api = _get_workspace_api()
        result = await api.lock_package(package=package, adom=adom)
        return {
            "status": "success",
            "message": f"Package '{package}' locked in ADOM '{adom}'",
            "warning": "Remember to commit or unlock when done!",
            "result": result,
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def unlock_policy_package_workspace(
    package: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Unlock a policy package.
    
    **WARNING:** Unlocking without committing will discard all unsaved changes!
    
    Args:
        package: Policy package name
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with unlock operation result
    """
    try:
        api = _get_workspace_api()
        result = await api.unlock_package(package=package, adom=adom)
        return {
            "status": "success",
            "message": f"Package '{package}' unlocked in ADOM '{adom}'",
            "warning": "Any uncommitted changes have been discarded",
            "result": result,
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def commit_policy_package_workspace(
    package: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Commit changes to a policy package.
    
    Args:
        package: Policy package name
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with commit operation result
    """
    try:
        api = _get_workspace_api()
        result = await api.commit_package(package=package, adom=adom)
        return {
            "status": "success",
            "message": f"Changes committed to package '{package}' in ADOM '{adom}'",
            "reminder": "Don't forget to unlock the package",
            "result": result,
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_package_lock_status(
    package: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Get lock status for a policy package.
    
    Args:
        package: Policy package name
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with package lock information
    """
    try:
        api = _get_workspace_api()
        lock_info = await api.get_package_lock_info(package=package, adom=adom)
        return {
            "status": "success",
            "package": package,
            "adom": adom,
            "lock_info": lock_info,
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


# ============================================================================
# Device Workspace Operations
# ============================================================================

@mcp.tool()
async def lock_device_workspace(
    device: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Lock a device for editing configuration.
    
    Args:
        device: Device name
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with lock operation result
        
    Example:
        result = lock_device_workspace(
            device="FGT-Branch-01",
            adom="production"
        )
    """
    try:
        api = _get_workspace_api()
        result = await api.lock_device(device=device, adom=adom)
        return {
            "status": "success",
            "message": f"Device '{device}' locked in ADOM '{adom}'",
            "warning": "Remember to commit or unlock when done!",
            "result": result,
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def unlock_device_workspace(
    device: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Unlock a device.
    
    **WARNING:** Unlocking without committing will discard all unsaved changes!
    
    Args:
        device: Device name
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with unlock operation result
    """
    try:
        api = _get_workspace_api()
        result = await api.unlock_device(device=device, adom=adom)
        return {
            "status": "success",
            "message": f"Device '{device}' unlocked in ADOM '{adom}'",
            "warning": "Any uncommitted changes have been discarded",
            "result": result,
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def commit_device_workspace(
    device: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Commit changes to a device configuration.
    
    Args:
        device: Device name
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with commit operation result
    """
    try:
        api = _get_workspace_api()
        result = await api.commit_device(device=device, adom=adom)
        return {
            "status": "success",
            "message": f"Changes committed to device '{device}' in ADOM '{adom}'",
            "reminder": "Don't forget to unlock the device",
            "result": result,
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


# ============================================================================
# ADOM Revision Operations
# ============================================================================

@mcp.tool()
async def revert_adom_to_revision(
    revision_version: int,
    adom: str = "root",
) -> dict[str, Any]:
    """Revert an ADOM to a previous revision.
    
    **DANGER:** This will discard ALL changes made after the specified revision!
    Use with extreme caution. Always verify the revision version first using
    list_adom_revisions.
    
    Args:
        revision_version: Revision version number to revert to
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with revert operation result
        
    Example:
        # First, list revisions to find the one you want
        revisions = list_adom_revisions(adom="production")
        # Then revert to a specific version
        result = revert_adom_to_revision(
            revision_version=5,
            adom="production"
        )
    """
    try:
        api = _get_workspace_api()
        result = await api.revert_adom_revision(version=revision_version, adom=adom)
        return {
            "status": "success",
            "message": f"ADOM '{adom}' reverted to revision {revision_version}",
            "warning": "All changes after this revision have been discarded",
            "result": result,
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

