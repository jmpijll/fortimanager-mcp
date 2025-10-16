"""Monitoring and task management API module."""

import asyncio
from typing import Any

from fortimanager_mcp.api.client import FortiManagerClient
from fortimanager_mcp.api.models import SystemStatus, TaskStatus


class MonitoringAPI:
    """Monitoring and task management operations."""

    def __init__(self, client: FortiManagerClient) -> None:
        """Initialize monitoring API.

        Args:
            client: FortiManager client instance
        """
        self.client = client

    async def get_system_status(self) -> SystemStatus:
        """Get FortiManager system status.

        Returns:
            System status information
        """
        data = await self.client.get("/cli/global/system/status")
        return SystemStatus(**data)

    async def list_tasks(
        self,
        fields: list[str] | None = None,
        filter: list[Any] | None = None,
        limit: int | None = None,
    ) -> list[TaskStatus]:
        """List recent tasks.

        Args:
            fields: Specific fields to return
            filter: Filter criteria
            limit: Maximum number of tasks to return

        Returns:
            List of tasks
        """
        url = "/task/task"
        data = await self.client.get(url, fields=fields, filter=filter)

        if not isinstance(data, list):
            data = [data] if data else []

        # Apply limit if specified
        if limit and len(data) > limit:
            data = data[:limit]

        return [TaskStatus(**item) for item in data]

    async def get_task_status(self, task_id: int) -> TaskStatus:
        """Get specific task status.

        Args:
            task_id: Task ID

        Returns:
            Task status details
        """
        url = f"/task/task/{task_id}"
        data = await self.client.get(url)
        return TaskStatus(**data)

    async def wait_for_task(
        self,
        task_id: int,
        timeout: int = 300,
        poll_interval: int = 2,
    ) -> TaskStatus:
        """Wait for task to complete.

        Args:
            task_id: Task ID to wait for
            timeout: Maximum wait time in seconds
            poll_interval: Polling interval in seconds

        Returns:
            Final task status

        Raises:
            TimeoutError: If task doesn't complete within timeout
        """
        start_time = asyncio.get_event_loop().time()

        while True:
            task = await self.get_task_status(task_id)

            if task.is_complete:
                return task

            elapsed = asyncio.get_event_loop().time() - start_time
            if elapsed >= timeout:
                raise TimeoutError(f"Task {task_id} did not complete within {timeout}s")

            await asyncio.sleep(poll_interval)

    async def get_device_status(self, device: str, adom: str | None = None) -> dict[str, Any]:
        """Get device connectivity status.

        Args:
            device: Device name
            adom: ADOM name

        Returns:
            Device status information
        """
        url = f"/dvmdb/adom/{adom}/device/{device}" if adom else f"/dvmdb/device/{device}"
        data = await self.client.get(url, fields=["name", "conn_status", "ip", "os_ver"])
        return data

    async def check_pending_changes(self, adom: str = "root") -> dict[str, Any]:
        """Check for pending changes in ADOM.

        Args:
            adom: ADOM name

        Returns:
            Pending changes information
        """
        data = {
            "adom": adom,
        }
        result = await self.client.execute("/dvmdb/adom/workspace/check-pending-changes", data=data)
        return result

    # =========================================================================
    # ADOM Revision Control Methods
    # =========================================================================

    async def list_adom_revisions(self, adom: str = "root") -> list[dict[str, Any]]:
        """List configuration revisions for an ADOM.

        Args:
            adom: ADOM name

        Returns:
            List of revisions with metadata
        """
        url = f"/dvmdb/adom/{adom}/revision"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def get_adom_revision(
        self,
        revision_id: int | str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get details of a specific revision.

        Args:
            revision_id: Revision ID or version number
            adom: ADOM name

        Returns:
            Revision details
        """
        url = f"/dvmdb/adom/{adom}/revision/{revision_id}"
        data = await self.client.get(url)
        return data if isinstance(data, dict) else {}

    async def create_adom_revision(
        self,
        adom: str = "root",
        name: str | None = None,
        description: str | None = None,
    ) -> dict[str, Any]:
        """Create a new configuration revision snapshot.

        Args:
            adom: ADOM name
            name: Optional revision name
            description: Optional description

        Returns:
            Created revision details
        """
        url = f"/dvmdb/adom/{adom}/revision"
        data_dict: dict[str, Any] = {}
        if name:
            data_dict["name"] = name
        if description:
            data_dict["desc"] = description
        
        result = await self.client.add(url, data_dict)
        return result if isinstance(result, dict) else {}

    # =========================================================================
    # Global Object Methods
    # =========================================================================

    async def list_global_firewall_addresses(self) -> list[dict[str, Any]]:
        """List global firewall addresses shared across all ADOMs.

        Returns:
            List of global firewall addresses
        """
        url = "/pm/config/global/obj/firewall/address"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def get_global_firewall_address(self, name: str) -> dict[str, Any]:
        """Get details of a specific global firewall address.

        Args:
            name: Address name

        Returns:
            Address details
        """
        url = f"/pm/config/global/obj/firewall/address/{name}"
        data = await self.client.get(url)
        return data if isinstance(data, dict) else {}

    async def list_global_firewall_services(self) -> list[dict[str, Any]]:
        """List global firewall services shared across all ADOMs.

        Returns:
            List of global firewall services
        """
        url = "/pm/config/global/obj/firewall/service/custom"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def get_global_firewall_service(self, name: str) -> dict[str, Any]:
        """Get details of a specific global firewall service.

        Args:
            name: Service name

        Returns:
            Service details
        """
        url = f"/pm/config/global/obj/firewall/service/custom/{name}"
        data = await self.client.get(url)
        return data if isinstance(data, dict) else {}

    async def list_global_address_groups(self) -> list[dict[str, Any]]:
        """List global address groups shared across all ADOMs.

        Returns:
            List of global address groups
        """
        url = "/pm/config/global/obj/firewall/addrgrp"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    # =========================================================================
    # Enhanced Task Query Methods
    # =========================================================================

    async def list_all_tasks(self, limit: int = 100) -> list[dict[str, Any]]:
        """List all tasks (not using Pydantic models for flexibility).

        Args:
            limit: Maximum number of tasks to return

        Returns:
            List of tasks as dictionaries
        """
        url = "/task/task"
        data = await self.client.get(url)
        
        if not isinstance(data, list):
            data = [data] if data else []
        
        # Apply limit
        if limit and len(data) > limit:
            data = data[:limit]
        
        return data

    async def get_task_details(self, task_id: int) -> dict[str, Any]:
        """Get detailed task information.

        Args:
            task_id: Task ID

        Returns:
            Task details as dictionary
        """
        url = f"/task/task/{task_id}"
        data = await self.client.get(url)
        return data if isinstance(data, dict) else {}

    async def list_running_tasks(self, limit: int = 50) -> list[dict[str, Any]]:
        """List currently running tasks.

        Args:
            limit: Maximum number of tasks to return

        Returns:
            List of running tasks
        """
        all_tasks = await self.list_all_tasks(limit=limit * 2)  # Get more to filter
        
        # Filter for running tasks (percent < 100)
        running = [t for t in all_tasks if t.get('percent', 100) < 100]
        
        return running[:limit]

    async def list_failed_tasks(self, limit: int = 50) -> list[dict[str, Any]]:
        """List failed tasks.

        Args:
            limit: Maximum number of tasks to return

        Returns:
            List of failed tasks
        """
        all_tasks = await self.list_all_tasks(limit=limit * 2)
        
        # Filter for failed tasks (state_flags contains error bits)
        failed = [t for t in all_tasks if t.get('state_flags', 0) & 0x02]  # Bit 1 = error
        
        return failed[:limit]

    # =========================================================================
    # Phase 37: Expanded Monitoring Operations
    # =========================================================================

    async def get_task_history(
        self,
        limit: int = 100,
        filter_type: str | None = None,
    ) -> list[dict[str, Any]]:
        """Get task execution history.
        
        Args:
            limit: Maximum number of tasks
            filter_type: Filter by task type
            
        Returns:
            List of historical tasks
        """
        url = "/task/task/history"
        params = {"limit": limit}
        if filter_type:
            params["filter"] = f"type=={filter_type}"
        data = await self.client.get(url, **params)
        return data if isinstance(data, list) else [data] if data else []

    async def get_system_performance_stats(self) -> dict[str, Any]:
        """Get detailed system performance statistics.
        
        Returns:
            System performance metrics
        """
        url = "/sys/performance/stats"
        return await self.client.get(url)

    async def get_device_connectivity_status(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """Get connectivity status for all devices.
        
        Args:
            adom: ADOM name
            
        Returns:
            Device connectivity status list
        """
        url = f"/dvmdb/adom/{adom}/device/connectivity"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def get_log_statistics(
        self,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get log storage and processing statistics.
        
        Args:
            adom: ADOM name
            
        Returns:
            Log statistics
        """
        url = f"/logview/adom/{adom}/stats"
        return await self.client.get(url)

    async def get_threat_statistics(
        self,
        adom: str = "root",
        time_range: str = "24h",
    ) -> dict[str, Any]:
        """Get threat detection statistics.
        
        Args:
            adom: ADOM name
            time_range: Time range (24h, 7d, 30d)
            
        Returns:
            Threat statistics
        """
        url = f"/monitor/adom/{adom}/threat/stats"
        params = {"range": time_range}
        return await self.client.get(url, **params)

    async def get_policy_hit_count(
        self,
        package: str,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """Get hit count statistics for policies.
        
        Args:
            package: Policy package name
            adom: ADOM name
            
        Returns:
            Policy hit counts
        """
        url = f"/monitor/adom/{adom}/pkg/{package}/policy/hitcount"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def get_bandwidth_statistics(
        self,
        device: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get bandwidth usage statistics for a device.
        
        Args:
            device: Device name
            adom: ADOM name
            
        Returns:
            Bandwidth statistics
        """
        url = f"/monitor/device/{device}/bandwidth"
        params = {"adom": adom}
        return await self.client.get(url, **params)

    async def get_session_statistics(
        self,
        device: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get session statistics for a device.
        
        Args:
            device: Device name
            adom: ADOM name
            
        Returns:
            Session statistics
        """
        url = f"/monitor/device/{device}/sessions"
        params = {"adom": adom}
        return await self.client.get(url, **params)

    async def get_alert_history(
        self,
        limit: int = 100,
    ) -> list[dict[str, Any]]:
        """Get system alert history.
        
        Args:
            limit: Maximum number of alerts
            
        Returns:
            Alert history
        """
        url = "/sys/alert/history"
        params = {"limit": limit}
        data = await self.client.get(url, **params)
        return data if isinstance(data, list) else [data] if data else []

    async def get_backup_status(self) -> dict[str, Any]:
        """Get backup status and history.
        
        Returns:
            Backup status information
        """
        url = "/sys/backup/status"
        return await self.client.get(url)

    async def get_ha_sync_status(self) -> dict[str, Any]:
        """Get HA synchronization status.
        
        Returns:
            HA sync status
        """
        url = "/sys/ha/sync-status"
        return await self.client.get(url)

    async def get_database_size(self) -> dict[str, Any]:
        """Get database size statistics.
        
        Returns:
            Database size information
        """
        url = "/sys/database/size"
        return await self.client.get(url)

    async def get_event_log(
        self,
        limit: int = 100,
        severity: str | None = None,
    ) -> list[dict[str, Any]]:
        """Get system event log.
        
        Args:
            limit: Maximum number of events
            severity: Filter by severity (critical, warning, info)
            
        Returns:
            System event log entries
        """
        url = "/sys/event/log"
        params = {"limit": limit}
        if severity:
            params["severity"] = severity
        data = await self.client.get(url, **params)
        return data if isinstance(data, list) else [data] if data else []

    async def get_firmware_upgrade_status(
        self,
        device: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get firmware upgrade status for a device.
        
        Args:
            device: Device name
            adom: ADOM name
            
        Returns:
            Firmware upgrade status
        """
        url = f"/monitor/device/{device}/firmware/upgrade-status"
        params = {"adom": adom}
        return await self.client.get(url, **params)

    async def get_configuration_changes(
        self,
        limit: int = 100,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """Get recent configuration changes.
        
        Args:
            limit: Maximum number of changes
            adom: ADOM name
            
        Returns:
            Configuration change history
        """
        url = f"/monitor/adom/{adom}/config/changes"
        params = {"limit": limit}
        data = await self.client.get(url, **params)
        return data if isinstance(data, list) else [data] if data else []

    # =========================================================================
    # Phase 42: Advanced Reporting & Analytics
    # =========================================================================

    async def get_system_resources(self) -> dict[str, Any]:
        """Get system resource usage (CPU, memory, disk).
        
        Returns:
            System resource statistics
        """
        url = "/sys/status"
        return await self.client.get(url)

    async def get_interface_statistics(
        self,
        interface: str | None = None,
    ) -> list[dict[str, Any]]:
        """Get network interface statistics.
        
        Args:
            interface: Specific interface name (optional)
            
        Returns:
            Interface statistics
        """
        url = "/sys/interface/stats"
        params = {}
        if interface:
            params["name"] = interface
        data = await self.client.get(url, **params)
        return data if isinstance(data, list) else [data] if data else []

    async def get_device_summary(
        self,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get summary of all devices in ADOM.
        
        Args:
            adom: ADOM name
            
        Returns:
            Device summary statistics
        """
        url = f"/dvmdb/adom/{adom}/summary"
        return await self.client.get(url)

    async def get_policy_summary(
        self,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get summary of policies in ADOM.
        
        Args:
            adom: ADOM name
            
        Returns:
            Policy summary statistics
        """
        url = f"/pm/config/adom/{adom}/summary"
        return await self.client.get(url)

    async def get_object_summary(
        self,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get summary of objects in ADOM.
        
        Args:
            adom: ADOM name
            
        Returns:
            Object summary statistics
        """
        url = f"/pm/config/adom/{adom}/obj/summary"
        return await self.client.get(url)

    async def get_admin_activity_log(
        self,
        limit: int = 100,
    ) -> list[dict[str, Any]]:
        """Get administrator activity log.
        
        Args:
            limit: Maximum entries
            
        Returns:
            Admin activity log entries
        """
        url = "/sys/admin/activity"
        params = {"limit": limit}
        data = await self.client.get(url, **params)
        return data if isinstance(data, list) else [data] if data else []

    async def get_system_uptime(self) -> dict[str, Any]:
        """Get system uptime and boot time.
        
        Returns:
            Uptime information
        """
        url = "/sys/status/uptime"
        return await self.client.get(url)

    async def get_cluster_status(self) -> dict[str, Any]:
        """Get HA cluster status if configured.
        
        Returns:
            Cluster status information
        """
        url = "/sys/ha/status"
        return await self.client.get(url)

    async def get_license_info(self) -> dict[str, Any]:
        """Get license and contract information.
        
        Returns:
            License details
        """
        url = "/sys/license"
        return await self.client.get(url)

    async def get_forticare_status(self) -> dict[str, Any]:
        """Get FortiCare registration status.
        
        Returns:
            FortiCare status
        """
        url = "/sys/forticare/status"
        return await self.client.get(url)

    async def get_global_policy_hit_stats(
        self,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get aggregated policy hit count statistics across all packages.
        
        Args:
            adom: ADOM name
            
        Returns:
            Global policy hit statistics
        """
        url = f"/monitor/adom/{adom}/policy/hit/global"
        return await self.client.get(url)

