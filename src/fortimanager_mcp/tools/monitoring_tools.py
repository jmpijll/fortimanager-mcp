"""MCP tools for monitoring and task management operations."""

import logging
from typing import Any

from fortimanager_mcp.api.monitoring import MonitoringAPI
from fortimanager_mcp.server import get_fmg_client, mcp

logger = logging.getLogger(__name__)


def _get_monitoring_api() -> MonitoringAPI:
    """Get MonitoringAPI instance."""
    client = get_fmg_client()
    if not client:
        raise RuntimeError("FortiManager client not initialized")
    return MonitoringAPI(client)


@mcp.tool()
async def get_system_status() -> dict[str, Any]:
    """Get FortiManager system status.

    Retrieves FortiManager system information including version, hostname,
    serial number, license status, and HA mode.

    Returns:
        Dictionary with system status information

    Example:
        result = get_system_status()
    """
    try:
        api = _get_monitoring_api()
        status = await api.get_system_status()

        return {
            "status": "success",
            "system": {
                "version": status.version,
                "hostname": status.hostname,
                "serial_number": status.serial,
                "admin_domain": status.admin_domain,
                "ha_mode": status.ha_mode,
                "license_status": status.license_status,
            },
        }
    except Exception as e:
        logger.error(f"Error getting system status: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def list_tasks(limit: int | None = None) -> dict[str, Any]:
    """List FortiManager tasks.

    Retrieves a list of recent tasks such as device installations,
    policy installations, and other operations.

    Args:
        limit: Maximum number of tasks to return (optional, defaults to all)

    Returns:
        Dictionary with list of tasks

    Example:
        result = list_tasks(limit=10)
    """
    try:
        api = _get_monitoring_api()
        tasks = await api.list_tasks(limit=limit)

        return {
            "status": "success",
            "count": len(tasks),
            "tasks": [
                {
                    "task_id": task.id,
                    "title": task.title,
                    "state": task.state,
                    "progress": task.percent,
                    "completed": task.num_done,
                    "total": task.num_lines,
                    "errors": task.num_err,
                    "warnings": task.num_warn,
                }
                for task in tasks
            ],
        }
    except Exception as e:
        logger.error(f"Error listing tasks: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def list_recent_tasks(limit: int = 10) -> dict[str, Any]:
    """List recent FortiManager tasks.

    Retrieves a list of recent tasks such as device installations,
    policy installations, and other operations.

    Args:
        limit: Maximum number of tasks to return (default: 10)

    Returns:
        Dictionary with list of recent tasks

    Example:
        result = list_recent_tasks(limit=20)
    """
    try:
        api = _get_monitoring_api()
        tasks = await api.list_tasks(limit=limit)

        return {
            "status": "success",
            "count": len(tasks),
            "tasks": [
                {
                    "task_id": task.id,
                    "title": task.title,
                    "state": task.state,
                    "progress": task.percent,
                    "completed": task.num_done,
                    "total": task.num_lines,
                    "errors": task.num_err,
                    "warnings": task.num_warn,
                }
                for task in tasks
            ],
        }
    except Exception as e:
        logger.error(f"Error listing tasks: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_task_status(task_id: int) -> dict[str, Any]:
    """Get detailed status of a specific task.

    Monitors the progress and status of a FortiManager task (e.g., device installation,
    policy installation). Use this to check if an installation has completed successfully.

    Args:
        task_id: Task ID to check

    Returns:
        Dictionary with detailed task status

    Example:
        result = get_task_status(task_id=2066)
    """
    try:
        api = _get_monitoring_api()
        task = await api.get_task_status(task_id=task_id)

        return {
            "status": "success",
            "task": {
                "task_id": task.id,
                "title": task.title,
                "state": task.state,
                "progress_percent": task.percent,
                "total_subtasks": task.num_lines,
                "completed_subtasks": task.num_done,
                "failed_subtasks": task.num_err,
                "warnings": task.num_warn,
                "is_running": task.is_running,
                "is_complete": task.is_complete,
                "is_successful": task.is_successful,
                "has_errors": task.has_errors,
                "start_time": task.start_tm,
                "end_time": task.end_tm,
                "duration_seconds": task.duration,
                "history": task.history,
            },
        }
    except Exception as e:
        logger.error(f"Error getting task {task_id} status: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def wait_for_task_completion(
    task_id: int,
    timeout: int = 300,
) -> dict[str, Any]:
    """Wait for a task to complete and return final status.

    Polls a task until it completes (success, failure, or cancelled).
    Useful for synchronous operations where you need to wait for results.

    Args:
        task_id: Task ID to wait for
        timeout: Maximum wait time in seconds (default: 300)

    Returns:
        Dictionary with final task status

    Example:
        result = wait_for_task_completion(task_id=2066, timeout=600)
    """
    try:
        api = _get_monitoring_api()
        task = await api.wait_for_task(task_id=task_id, timeout=timeout)

        return {
            "status": "success",
            "task": {
                "task_id": task.id,
                "title": task.title,
                "final_state": task.state,
                "is_successful": task.is_successful,
                "has_errors": task.has_errors,
                "failed_subtasks": task.num_err,
                "warnings": task.num_warn,
                "duration_seconds": task.duration,
            },
        }
    except Exception as e:
        logger.error(f"Error waiting for task {task_id}: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def check_device_connectivity(
    device: str,
    adom: str | None = None,
) -> dict[str, Any]:
    """Check device connectivity status.

    Verifies if a managed device is currently connected to FortiManager.
    Useful for troubleshooting connectivity issues.

    Args:
        device: Device name
        adom: Optional ADOM name

    Returns:
        Dictionary with device connectivity status

    Example:
        result = check_device_connectivity(device="FGT-Branch-01", adom="root")
    """
    try:
        api = _get_monitoring_api()
        device_status = await api.get_device_status(device=device, adom=adom)

        conn_status = device_status.get("conn_status")
        is_connected = conn_status == 1

        return {
            "status": "success",
            "device": {
                "name": device_status.get("name"),
                "ip": device_status.get("ip"),
                "os_version": device_status.get("os_ver"),
                "connection_status": conn_status,
                "is_connected": is_connected,
                "status_text": "Connected" if is_connected else "Disconnected",
            },
        }
    except Exception as e:
        logger.error(f"Error checking device {device} connectivity: {e}")
        return {"status": "error", "message": str(e)}


# =============================================================================
# ADOM Revision Control Tools
# =============================================================================


@mcp.tool()
async def list_adom_revisions(adom: str = "root") -> dict[str, Any]:
    """List all configuration revisions for an ADOM.
    
    Configuration revisions are snapshots of ADOM configuration at specific
    points in time. They provide:
    - Version control for configurations
    - Ability to rollback changes
    - Configuration history tracking
    - Change documentation
    
    Use cases:
    - Review configuration history
    - Identify when changes were made
    - Prepare for rollback operations
    - Audit configuration changes
    
    Args:
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with status and list of revisions
    """
    try:
        api = _get_monitoring_api()
        revisions = await api.list_adom_revisions(adom=adom)
        return {
            "status": "success",
            "count": len(revisions),
            "revisions": revisions,
        }
    except Exception as e:
        logger.error(f"Error listing ADOM revisions: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_adom_revision(
    revision_id: int,
    adom: str = "root",
) -> dict[str, Any]:
    """Get detailed information about a specific configuration revision.
    
    Args:
        revision_id: Revision ID number
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with status and revision details
    """
    try:
        api = _get_monitoring_api()
        revision = await api.get_adom_revision(revision_id=revision_id, adom=adom)
        return {
            "status": "success",
            "revision": revision,
        }
    except Exception as e:
        logger.error(f"Error getting revision {revision_id}: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def create_adom_revision(
    adom: str = "root",
    name: str | None = None,
    description: str | None = None,
) -> dict[str, Any]:
    """Create a new configuration revision snapshot.
    
    Creates a point-in-time snapshot of the current ADOM configuration.
    This is useful before making significant changes to enable rollback.
    
    Best practices:
    - Create revision before major changes
    - Include descriptive name and notes
    - Document the reason for the snapshot
    - Regular snapshots for change tracking
    
    Args:
        adom: ADOM name (default: root)
        name: Optional revision name/label
        description: Optional description of why revision was created
    
    Returns:
        Dictionary with status and created revision details
    """
    try:
        api = _get_monitoring_api()
        revision = await api.create_adom_revision(
            adom=adom,
            name=name,
            description=description,
        )
        return {
            "status": "success",
            "revision": revision,
        }
    except Exception as e:
        logger.error(f"Error creating revision: {e}")
        return {"status": "error", "message": str(e)}


# =============================================================================
# Global Object Tools
# =============================================================================


@mcp.tool()
async def list_global_firewall_addresses() -> dict[str, Any]:
    """List global firewall addresses shared across all ADOMs.
    
    Global objects are defined at the FortiManager level and can be
    used by all ADOMs. This provides:
    - Centralized object management
    - Consistent definitions across ADOMs
    - Reduced duplication
    - Easier maintenance
    
    Common global objects include:
    - Public IP ranges
    - Known threat actor IPs
    - Common service providers
    - Standard network ranges
    
    Returns:
        Dictionary with status and list of global addresses
    """
    try:
        api = _get_monitoring_api()
        addresses = await api.list_global_firewall_addresses()
        return {
            "status": "success",
            "count": len(addresses),
            "addresses": addresses,
        }
    except Exception as e:
        logger.error(f"Error listing global addresses: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_global_firewall_address(name: str) -> dict[str, Any]:
    """Get details of a specific global firewall address.
    
    Args:
        name: Address object name
    
    Returns:
        Dictionary with status and address details
    """
    try:
        api = _get_monitoring_api()
        address = await api.get_global_firewall_address(name=name)
        return {
            "status": "success",
            "address": address,
        }
    except Exception as e:
        logger.error(f"Error getting global address {name}: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def list_global_firewall_services() -> dict[str, Any]:
    """List global firewall services shared across all ADOMs.
    
    Global services are firewall service objects available to all ADOMs,
    typically used for:
    - Custom application ports
    - Non-standard service definitions
    - Organization-wide services
    - Common third-party applications
    
    Returns:
        Dictionary with status and list of global services
    """
    try:
        api = _get_monitoring_api()
        services = await api.list_global_firewall_services()
        return {
            "status": "success",
            "count": len(services),
            "services": services,
        }
    except Exception as e:
        logger.error(f"Error listing global services: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_global_firewall_service(name: str) -> dict[str, Any]:
    """Get details of a specific global firewall service.
    
    Args:
        name: Service object name
    
    Returns:
        Dictionary with status and service details
    """
    try:
        api = _get_monitoring_api()
        service = await api.get_global_firewall_service(name=name)
        return {
            "status": "success",
            "service": service,
        }
    except Exception as e:
        logger.error(f"Error getting global service {name}: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def list_global_address_groups() -> dict[str, Any]:
    """List global address groups shared across all ADOMs.
    
    Global address groups contain multiple addresses and are available
    to all ADOMs for consistent policy application.
    
    Returns:
        Dictionary with status and list of global address groups
    """
    try:
        api = _get_monitoring_api()
        groups = await api.list_global_address_groups()
        return {
            "status": "success",
            "count": len(groups),
            "groups": groups,
        }
    except Exception as e:
        logger.error(f"Error listing global address groups: {e}")
        return {"status": "error", "message": str(e)}


# =============================================================================
# Enhanced Task Query Tools
# =============================================================================


@mcp.tool()
async def list_all_tasks(limit: int = 100) -> dict[str, Any]:
    """List all recent tasks with flexible limit.
    
    Retrieves task history from FortiManager including:
    - Policy installations
    - Device operations
    - Configuration changes
    - Script executions
    - Backup operations
    
    Args:
        limit: Maximum number of tasks to return (default: 100)
    
    Returns:
        Dictionary with status and list of tasks
    """
    try:
        api = _get_monitoring_api()
        tasks = await api.list_all_tasks(limit=limit)
        return {
            "status": "success",
            "count": len(tasks),
            "tasks": tasks,
        }
    except Exception as e:
        logger.error(f"Error listing all tasks: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_task_details(task_id: int) -> dict[str, Any]:
    """Get comprehensive details about a specific task.
    
    Provides full task information including:
    - Task type and title
    - Start and end times
    - Progress percentage
    - Status and state
    - Associated devices/ADOMs
    - Error messages (if failed)
    
    Args:
        task_id: Task ID number
    
    Returns:
        Dictionary with status and detailed task information
    """
    try:
        api = _get_monitoring_api()
        task = await api.get_task_details(task_id=task_id)
        return {
            "status": "success",
            "task": task,
        }
    except Exception as e:
        logger.error(f"Error getting task {task_id} details: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def list_running_tasks(limit: int = 50) -> dict[str, Any]:
    """List currently running (in-progress) tasks.
    
    Filters tasks to show only those currently executing.
    Useful for:
    - Monitoring active operations
    - Identifying long-running tasks
    - Checking operation progress
    - Troubleshooting delays
    
    Args:
        limit: Maximum number of tasks to return (default: 50)
    
    Returns:
        Dictionary with status and list of running tasks
    """
    try:
        api = _get_monitoring_api()
        tasks = await api.list_running_tasks(limit=limit)
        return {
            "status": "success",
            "count": len(tasks),
            "running_tasks": tasks,
        }
    except Exception as e:
        logger.error(f"Error listing running tasks: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def list_failed_tasks(limit: int = 50) -> dict[str, Any]:
    """List recently failed tasks.
    
    Returns tasks that encountered errors or failed to complete.
    Essential for:
    - Troubleshooting failures
    - Identifying recurring issues
    - Monitoring system health
    - Alerting on problems
    
    Args:
        limit: Maximum number of tasks to return (default: 50)
    
    Returns:
        Dictionary with status and list of failed tasks
    """
    try:
        api = _get_monitoring_api()
        tasks = await api.list_failed_tasks(limit=limit)
        return {
            "status": "success",
            "count": len(tasks),
            "failed_tasks": tasks,
        }
    except Exception as e:
        logger.error(f"Error listing failed tasks: {e}")
        return {"status": "error", "message": str(e)}


# =============================================================================
# Phase 37: Expanded Monitoring Tools
# =============================================================================


@mcp.tool()
async def get_task_history(limit: int = 100, filter_type: str | None = None) -> dict[str, Any]:
    """Get task execution history with optional filtering.
    
    Retrieves historical task records for audit and analysis.
    
    Args:
        limit: Maximum number of tasks (default: 100)
        filter_type: Optional task type filter
    
    Returns:
        Dictionary with task history
    """
    try:
        api = _get_monitoring_api()
        history = await api.get_task_history(limit=limit, filter_type=filter_type)
        return {"status": "success", "count": len(history), "history": history}
    except Exception as e:
        logger.error(f"Error getting task history: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_system_performance_stats() -> dict[str, Any]:
    """Get detailed system performance statistics including CPU, memory, and disk."""
    try:
        api = _get_monitoring_api()
        stats = await api.get_system_performance_stats()
        return {"status": "success", "performance": stats}
    except Exception as e:
        logger.error(f"Error getting performance stats: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_device_connectivity_status(adom: str = "root") -> dict[str, Any]:
    """Get connectivity status for all managed devices in an ADOM."""
    try:
        api = _get_monitoring_api()
        status = await api.get_device_connectivity_status(adom=adom)
        return {"status": "success", "devices": status}
    except Exception as e:
        logger.error(f"Error getting device connectivity: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_log_statistics(adom: str = "root") -> dict[str, Any]:
    """Get log storage and processing statistics for an ADOM."""
    try:
        api = _get_monitoring_api()
        stats = await api.get_log_statistics(adom=adom)
        return {"status": "success", "log_stats": stats}
    except Exception as e:
        logger.error(f"Error getting log statistics: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_threat_statistics(adom: str = "root", time_range: str = "24h") -> dict[str, Any]:
    """Get threat detection statistics for specified time range (24h, 7d, 30d)."""
    try:
        api = _get_monitoring_api()
        stats = await api.get_threat_statistics(adom=adom, time_range=time_range)
        return {"status": "success", "threat_stats": stats}
    except Exception as e:
        logger.error(f"Error getting threat statistics: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_policy_hit_count(package: str, adom: str = "root") -> dict[str, Any]:
    """Get hit count statistics showing which policies are actively used."""
    try:
        api = _get_monitoring_api()
        hits = await api.get_policy_hit_count(package=package, adom=adom)
        return {"status": "success", "hit_counts": hits}
    except Exception as e:
        logger.error(f"Error getting policy hit counts: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_bandwidth_statistics(device: str, adom: str = "root") -> dict[str, Any]:
    """Get bandwidth usage statistics for a specific device."""
    try:
        api = _get_monitoring_api()
        stats = await api.get_bandwidth_statistics(device=device, adom=adom)
        return {"status": "success", "bandwidth": stats}
    except Exception as e:
        logger.error(f"Error getting bandwidth statistics: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_session_statistics(device: str, adom: str = "root") -> dict[str, Any]:
    """Get session statistics for a specific device."""
    try:
        api = _get_monitoring_api()
        stats = await api.get_session_statistics(device=device, adom=adom)
        return {"status": "success", "sessions": stats}
    except Exception as e:
        logger.error(f"Error getting session statistics: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_alert_history(limit: int = 100) -> dict[str, Any]:
    """Get system alert history."""
    try:
        api = _get_monitoring_api()
        alerts = await api.get_alert_history(limit=limit)
        return {"status": "success", "count": len(alerts), "alerts": alerts}
    except Exception as e:
        logger.error(f"Error getting alert history: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_backup_status() -> dict[str, Any]:
    """Get backup status and history."""
    try:
        api = _get_monitoring_api()
        backup_info = await api.get_backup_status()
        return {"status": "success", "backup": backup_info}
    except Exception as e:
        logger.error(f"Error getting backup status: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_ha_sync_status() -> dict[str, Any]:
    """Get High Availability synchronization status."""
    try:
        api = _get_monitoring_api()
        ha_status = await api.get_ha_sync_status()
        return {"status": "success", "ha_sync": ha_status}
    except Exception as e:
        logger.error(f"Error getting HA sync status: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_database_size() -> dict[str, Any]:
    """Get database size statistics."""
    try:
        api = _get_monitoring_api()
        db_size = await api.get_database_size()
        return {"status": "success", "database_size": db_size}
    except Exception as e:
        logger.error(f"Error getting database size: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_event_log(limit: int = 100, severity: str | None = None) -> dict[str, Any]:
    """Get system event log with optional severity filter (critical, warning, info)."""
    try:
        api = _get_monitoring_api()
        events = await api.get_event_log(limit=limit, severity=severity)
        return {"status": "success", "count": len(events), "events": events}
    except Exception as e:
        logger.error(f"Error getting event log: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_firmware_upgrade_status(device: str, adom: str = "root") -> dict[str, Any]:
    """Get firmware upgrade status for a specific device."""
    try:
        api = _get_monitoring_api()
        status = await api.get_firmware_upgrade_status(device=device, adom=adom)
        return {"status": "success", "firmware_status": status}
    except Exception as e:
        logger.error(f"Error getting firmware upgrade status: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_configuration_changes(limit: int = 100, adom: str = "root") -> dict[str, Any]:
    """Get recent configuration changes for audit trail."""
    try:
        api = _get_monitoring_api()
        changes = await api.get_configuration_changes(limit=limit, adom=adom)
        return {"status": "success", "count": len(changes), "changes": changes}
    except Exception as e:
        logger.error(f"Error getting configuration changes: {e}")
        return {"status": "error", "message": str(e)}


# =============================================================================
# Phase 42: Advanced Reporting & Analytics
# =============================================================================


@mcp.tool()
async def get_system_resource_usage() -> dict[str, Any]:
    """Get system resource usage including CPU, memory, and disk statistics."""
    try:
        api = _get_monitoring_api()
        resources = await api.get_system_resources()
        return {"status": "success", "resources": resources}
    except Exception as e:
        logger.error(f"Error getting system resources: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_network_interface_stats(interface: str | None = None) -> dict[str, Any]:
    """Get network interface statistics with optional interface filter."""
    try:
        api = _get_monitoring_api()
        stats = await api.get_interface_statistics(interface=interface)
        return {"status": "success", "interface_stats": stats}
    except Exception as e:
        logger.error(f"Error getting interface statistics: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_adom_device_summary(adom: str = "root") -> dict[str, Any]:
    """Get summary statistics of all devices in an ADOM."""
    try:
        api = _get_monitoring_api()
        summary = await api.get_device_summary(adom=adom)
        return {"status": "success", "device_summary": summary}
    except Exception as e:
        logger.error(f"Error getting device summary: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_adom_policy_summary(adom: str = "root") -> dict[str, Any]:
    """Get summary statistics of all policies in an ADOM."""
    try:
        api = _get_monitoring_api()
        summary = await api.get_policy_summary(adom=adom)
        return {"status": "success", "policy_summary": summary}
    except Exception as e:
        logger.error(f"Error getting policy summary: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_adom_object_summary(adom: str = "root") -> dict[str, Any]:
    """Get summary statistics of all objects in an ADOM."""
    try:
        api = _get_monitoring_api()
        summary = await api.get_object_summary(adom=adom)
        return {"status": "success", "object_summary": summary}
    except Exception as e:
        logger.error(f"Error getting object summary: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_administrator_activity(limit: int = 100) -> dict[str, Any]:
    """Get administrator activity log for audit purposes."""
    try:
        api = _get_monitoring_api()
        activity = await api.get_admin_activity_log(limit=limit)
        return {"status": "success", "count": len(activity), "activity_log": activity}
    except Exception as e:
        logger.error(f"Error getting admin activity: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_fmg_uptime() -> dict[str, Any]:
    """Get FortiManager system uptime and boot time."""
    try:
        api = _get_monitoring_api()
        uptime = await api.get_system_uptime()
        return {"status": "success", "uptime": uptime}
    except Exception as e:
        logger.error(f"Error getting system uptime: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_ha_cluster_status() -> dict[str, Any]:
    """Get High Availability cluster status if configured."""
    try:
        api = _get_monitoring_api()
        cluster = await api.get_cluster_status()
        return {"status": "success", "cluster_status": cluster}
    except Exception as e:
        logger.error(f"Error getting cluster status: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_fmg_license() -> dict[str, Any]:
    """Get FortiManager license and contract information."""
    try:
        api = _get_monitoring_api()
        license_info = await api.get_license_info()
        return {"status": "success", "license": license_info}
    except Exception as e:
        logger.error(f"Error getting license info: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_forticare_registration() -> dict[str, Any]:
    """Get FortiCare registration and support status."""
    try:
        api = _get_monitoring_api()
        forticare = await api.get_forticare_status()
        return {"status": "success", "forticare_status": forticare}
    except Exception as e:
        logger.error(f"Error getting FortiCare status: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_global_policy_hit_statistics(adom: str = "root") -> dict[str, Any]:
    """Get aggregated policy hit count statistics across all policy packages.
    
    Args:
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with global policy hit statistics
    """
    try:
        api = _get_monitoring_api()
        stats = await api.get_global_policy_hit_stats(adom=adom)
        return {"status": "success", "adom": adom, "global_policy_hits": stats}
    except Exception as e:
        logger.error(f"Error getting global policy hit statistics: {e}")
        return {"status": "error", "message": str(e)}
