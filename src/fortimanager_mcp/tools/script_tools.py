"""MCP tools for CLI script management operations."""

import logging
from typing import Any

from fortimanager_mcp.api.scripts import ScriptAPI
from fortimanager_mcp.server import get_fmg_client, mcp

logger = logging.getLogger(__name__)


def _get_script_api() -> ScriptAPI:
    """Get ScriptAPI instance."""
    client = get_fmg_client()
    if not client:
        raise RuntimeError("FortiManager client not initialized")
    return ScriptAPI(client)


@mcp.tool()
async def list_cli_scripts(adom: str = "root") -> dict[str, Any]:
    """List CLI scripts in an ADOM.
    
    CLI scripts automate configuration tasks and can target:
    - Policy packages or ADOM database
    - Device database  
    - Remote devices directly
    
    Args:
        adom: ADOM name (default: "root")
        
    Returns:
        Dictionary with list of CLI scripts
        
    Example:
        result = list_cli_scripts(adom="root")
    """
    try:
        api = _get_script_api()
        scripts = await api.list_scripts(adom=adom)
        
        return {
            "status": "success",
            "count": len(scripts),
            "scripts": scripts,
        }
    except Exception as e:
        logger.error(f"Failed to list CLI scripts: {e}")
        return {
            "status": "error",
            "message": str(e),
        }


@mcp.tool()
async def get_cli_script(
    name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Get CLI script details.
    
    Retrieves detailed information about a specific CLI script including
    its content, target, type, and description.
    
    Args:
        name: Script name
        adom: ADOM name (default: "root")
        
    Returns:
        Dictionary with script details
        
    Example:
        result = get_cli_script(name="my_script", adom="root")
    """
    try:
        api = _get_script_api()
        script = await api.get_script(name=name, adom=adom)
        
        return {
            "status": "success",
            "script": script,
        }
    except Exception as e:
        logger.error(f"Failed to get CLI script: {e}")
        return {
            "status": "error",
            "message": str(e),
        }


@mcp.tool()
async def create_cli_script(
    name: str,
    content: str,
    target: str,
    adom: str = "root",
    script_type: str = "cli",
    description: str | None = None,
) -> dict[str, Any]:
    """Create a new CLI script.
    
    Creates a CLI script that can automate configuration tasks.
    Scripts can be regular CLI commands or Jinja templates.
    
    Args:
        name: Script name
        content: Script content (CLI commands or Jinja template)
        target: Script target:
               - "adom_database": Policy Package or ADOM Database
               - "device_database": Device Database
               - "remote_device": Remote FortiGate Directly (via CLI)
        adom: ADOM name (default: "root")
        script_type: Script type - "cli" or "jinja" (default: "cli")
        description: Optional script description
        
    Returns:
        Dictionary with created script details
        
    Example:
        result = create_cli_script(
            name="add_vlan",
            content="config system interface\\nedit vlan10\\nset vdom root\\nend",
            target="remote_device",
            adom="root",
            description="Add VLAN 10 interface"
        )
    """
    try:
        api = _get_script_api()
        script = await api.create_script(
            name=name,
            content=content,
            target=target,
            adom=adom,
            script_type=script_type,
            description=description,
        )
        
        return {
            "status": "success",
            "script": script,
        }
    except Exception as e:
        logger.error(f"Failed to create CLI script: {e}")
        return {
            "status": "error",
            "message": str(e),
        }


@mcp.tool()
async def update_cli_script(
    name: str,
    adom: str = "root",
    content: str | None = None,
    description: str | None = None,
) -> dict[str, Any]:
    """Update an existing CLI script.
    
    Modifies properties of an existing CLI script.
    Only specified fields will be updated.
    
    Args:
        name: Script name
        adom: ADOM name (default: "root")
        content: Updated script content
        description: Updated description
        
    Returns:
        Dictionary with updated script details
        
    Example:
        result = update_cli_script(
            name="add_vlan",
            adom="root",
            description="Updated description"
        )
    """
    try:
        api = _get_script_api()
        script = await api.update_script(
            name=name,
            adom=adom,
            content=content,
            description=description,
        )
        
        return {
            "status": "success",
            "script": script,
        }
    except Exception as e:
        logger.error(f"Failed to update CLI script: {e}")
        return {
            "status": "error",
            "message": str(e),
        }


@mcp.tool()
async def delete_cli_script(
    name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Delete a CLI script.
    
    Removes a CLI script from FortiManager.
    
    Args:
        name: Script name
        adom: ADOM name (default: "root")
        
    Returns:
        Dictionary with deletion status
        
    Example:
        result = delete_cli_script(name="add_vlan", adom="root")
    """
    try:
        api = _get_script_api()
        await api.delete_script(name=name, adom=adom)
        
        return {
            "status": "success",
            "message": f"Script '{name}' deleted successfully",
        }
    except Exception as e:
        logger.error(f"Failed to delete CLI script: {e}")
        return {
            "status": "error",
            "message": str(e),
        }


@mcp.tool()
async def execute_cli_script(
    script: str,
    adom: str = "root",
    package: str | None = None,
    device: str | None = None,
) -> dict[str, Any]:
    """Execute a CLI script.
    
    Runs a CLI script against a policy package, ADOM database, or device.
    The execution creates a task that can be monitored.
    
    Args:
        script: Script name to execute
        adom: ADOM name (default: "root")
        package: Policy package name (for adom_database target)
        device: Device name (for remote_device target)
        
    Returns:
        Dictionary with task ID and execution status
        
    Notes:
        - For ADOM database: Don't specify package or device
        - For policy package: Specify package name
        - For device: Specify device name
        
    Log ID calculation:
        - ADOM/Package DB: log_id = str(task_id) + "1"
        - Device: log_id = str(task_id) + "0"
        
    Example:
        # Execute against policy package
        result = execute_cli_script(
            script="my_script",
            adom="root",
            package="default"
        )
        
        # Execute against device
        result = execute_cli_script(
            script="my_script",
            adom="root",
            device="FGT-Branch-01"
        )
    """
    try:
        api = _get_script_api()
        
        # Build scope for device execution
        scope = None
        if device:
            scope = [{"name": device, "vdom": "global"}]
        
        result = await api.execute_script(
            script=script,
            adom=adom,
            package=package,
            scope=scope,
        )
        
        task_id = result.get("task")
        
        # Calculate log ID
        log_id = None
        if task_id:
            if device:
                log_id = int(str(task_id) + "0")
            else:
                log_id = int(str(task_id) + "1")
        
        return {
            "status": "success",
            "task_id": task_id,
            "log_id": log_id,
            "message": f"Script '{script}' execution started (task {task_id})",
        }
    except Exception as e:
        logger.error(f"Failed to execute CLI script: {e}")
        return {
            "status": "error",
            "message": str(e),
        }


@mcp.tool()
async def get_cli_script_log(log_id: int) -> dict[str, Any]:
    """Get CLI script execution log.
    
    Retrieves the execution log for a completed CLI script run.
    The log_id is calculated from the task_id:
    - For ADOM/Package DB: log_id = str(task_id) + "1"
    - For device: log_id = str(task_id) + "0"
    
    Args:
        log_id: Log ID (from execute_cli_script result)
        
    Returns:
        Dictionary with script execution log
        
    Example:
        result = get_cli_script_log(log_id=4521)
    """
    try:
        api = _get_script_api()
        log = await api.get_script_log(log_id=log_id)
        
        return {
            "status": "success",
            "log": log,
        }
    except Exception as e:
        logger.error(f"Failed to get CLI script log: {e}")
        return {
            "status": "error",
            "message": str(e),
        }


# ==============================================================================
# Phase 24: Complete CLI Script Management
# ==============================================================================


@mcp.tool()
async def clone_cli_script(
    source_name: str,
    new_name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Clone an existing CLI script with a new name.
    
    Creates a copy of an existing script, useful for:
    - Creating variations of a script
    - Backing up before modifications
    - Template duplication
    
    Args:
        source_name: Name of the script to clone
        new_name: Name for the cloned script
        adom: ADOM name (default: "root")
    
    Returns:
        Dictionary with cloned script details
    
    Example:
        result = clone_cli_script(
            source_name="base_config",
            new_name="branch_config",
            adom="root"
        )
    """
    try:
        api = _get_script_api()
        script = await api.clone_script(
            source_name=source_name,
            new_name=new_name,
            adom=adom,
        )
        
        return {
            "status": "success",
            "message": f"Script '{source_name}' cloned to '{new_name}'",
            "script": script,
        }
    except Exception as e:
        logger.error(f"Failed to clone CLI script: {e}")
        return {
            "status": "error",
            "message": str(e),
        }


@mcp.tool()
async def list_cli_script_history(
    adom: str = "root",
    limit: int = 100,
) -> dict[str, Any]:
    """List CLI script execution history.
    
    Retrieves execution history for all scripts in an ADOM, showing:
    - Script name
    - Execution time
    - Target (device, package, ADOM)
    - Execution status
    - User who executed
    
    Args:
        adom: ADOM name (default: "root")
        limit: Maximum number of records to return (default: 100)
    
    Returns:
        Dictionary with execution history
    
    Example:
        result = list_cli_script_history(adom="root", limit=50)
    """
    try:
        api = _get_script_api()
        history = await api.list_script_history(adom=adom, limit=limit)
        
        return {
            "status": "success",
            "count": len(history),
            "history": history,
        }
    except Exception as e:
        logger.error(f"Failed to list CLI script history: {e}")
        return {
            "status": "error",
            "message": str(e),
        }


@mcp.tool()
async def get_cli_script_history(
    script_name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Get execution history for a specific CLI script.
    
    Retrieves all execution records for a particular script,
    useful for auditing and troubleshooting.
    
    Args:
        script_name: Name of the script
        adom: ADOM name (default: "root")
    
    Returns:
        Dictionary with script's execution history
    
    Example:
        result = get_cli_script_history(
            script_name="daily_backup",
            adom="root"
        )
    """
    try:
        api = _get_script_api()
        history = await api.get_script_history(
            script_name=script_name,
            adom=adom,
        )
        
        return {
            "status": "success",
            "script": script_name,
            "executions": len(history),
            "history": history,
        }
    except Exception as e:
        logger.error(f"Failed to get script history: {e}")
        return {
            "status": "error",
            "message": str(e),
        }


@mcp.tool()
async def validate_cli_script(
    name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Validate CLI script syntax before execution.
    
    Checks the script for syntax errors without executing it,
    helping prevent errors during actual execution.
    
    Args:
        name: Script name
        adom: ADOM name (default: "root")
    
    Returns:
        Dictionary with validation results
    
    Example:
        result = validate_cli_script(
            name="my_script",
            adom="root"
        )
    """
    try:
        api = _get_script_api()
        validation = await api.validate_script(name=name, adom=adom)
        
        return {
            "status": "success",
            "script": name,
            "validation": validation,
        }
    except Exception as e:
        logger.error(f"Failed to validate CLI script: {e}")
        return {
            "status": "error",
            "message": str(e),
        }


@mcp.tool()
async def schedule_cli_script(
    script: str,
    schedule_time: str,
    adom: str = "root",
    package: str | None = None,
    device: str | None = None,
) -> dict[str, Any]:
    """Schedule a CLI script for future execution.
    
    Schedules a script to run at a specified time, useful for:
    - Maintenance windows
    - Off-hours configuration changes
    - Automated periodic tasks
    
    Args:
        script: Script name
        schedule_time: Execution time in format "YYYY-MM-DD HH:MM:SS"
        adom: ADOM name (default: "root")
        package: Policy package name (for adom_database target)
        device: Device name (for remote_device target)
    
    Returns:
        Dictionary with scheduled task information
    
    Example:
        result = schedule_cli_script(
            script="maintenance_script",
            schedule_time="2025-10-17 02:00:00",
            adom="root",
            device="FGT-HQ-01"
        )
    """
    try:
        api = _get_script_api()
        
        # Build scope for device execution
        scope = None
        if device:
            scope = [{"name": device, "vdom": "global"}]
        
        scheduled = await api.schedule_script_execution(
            script=script,
            schedule_time=schedule_time,
            adom=adom,
            package=package,
            scope=scope,
        )
        
        return {
            "status": "success",
            "message": f"Script '{script}' scheduled for {schedule_time}",
            "task": scheduled,
        }
    except Exception as e:
        logger.error(f"Failed to schedule CLI script: {e}")
        return {
            "status": "error",
            "message": str(e),
        }

