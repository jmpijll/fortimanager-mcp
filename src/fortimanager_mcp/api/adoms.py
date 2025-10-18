"""ADOM management API module."""

from typing import Any

from fortimanager_mcp.api.client import FortiManagerClient
from fortimanager_mcp.api.models import ADOM
from fortimanager_mcp.utils.errors import ResourceNotFoundError


class ADOMAPI:
    """ADOM (Administrative Domain) management operations."""

    def __init__(self, client: FortiManagerClient) -> None:
        """Initialize ADOM API.

        Args:
            client: FortiManager client instance
        """
        self.client = client

    async def list_adoms(
        self,
        fields: list[str] | None = None,
        filter: list[Any] | None = None,
    ) -> list[ADOM]:
        """List all ADOMs.

        Args:
            fields: Specific fields to return
            filter: Filter criteria

        Returns:
            List of ADOMs
        """
        data = await self.client.get("/dvmdb/adom", fields=fields, filter=filter)
        if not isinstance(data, list):
            data = [data] if data else []

        return [ADOM(**item) for item in data]

    async def get_adom(self, name: str) -> ADOM:
        """Get specific ADOM details.

        Args:
            name: ADOM name

        Returns:
            ADOM details
        """
        data = await self.client.get(f"/dvmdb/adom/{name}")
        return ADOM(**data)

    async def create_adom(
        self,
        name: str,
        description: str | None = None,
        os_ver: str = "7.0",
        mr: int = 0,
        **kwargs: Any,
    ) -> ADOM:
        """Create new ADOM.

        Args:
            name: ADOM name
            description: ADOM description
            os_ver: FortiOS version
            mr: Maintenance release
            **kwargs: Additional ADOM parameters

        Returns:
            Created ADOM
        """
        data = {
            "name": name,
            "os_ver": os_ver,
            "mr": mr,
            **kwargs,
        }

        if description:
            data["desc"] = description

        await self.client.add("/dvmdb/adom", data=data)
        return await self.get_adom(name)

    async def update_adom(self, name: str, **kwargs: Any) -> ADOM:
        """Update ADOM settings.

        Args:
            name: ADOM name
            **kwargs: ADOM parameters to update

        Returns:
            Updated ADOM
        """
        await self.client.set(f"/dvmdb/adom/{name}", data=kwargs)
        return await self.get_adom(name)

    async def delete_adom(self, name: str) -> None:
        """Delete ADOM.

        Args:
            name: ADOM name
        """
        await self.client.delete(f"/dvmdb/adom/{name}")

    async def lock_adom(self, name: str) -> None:
        """Lock ADOM for editing (workspace mode).

        Args:
            name: ADOM name
        """
        data = {"adom": name}
        await self.client.execute("/dvmdb/adom/workspace/lock", data=data)

    async def unlock_adom(self, name: str) -> None:
        """Unlock ADOM (workspace mode).

        Args:
            name: ADOM name
        """
        data = {"adom": name}
        await self.client.execute("/dvmdb/adom/workspace/unlock", data=data)

    async def commit_adom(self, name: str) -> None:
        """Commit ADOM changes (workspace mode).

        Args:
            name: ADOM name
        """
        data = {"adom": name}
        await self.client.execute("/dvmdb/adom/workspace/commit", data=data)

    # Advanced ADOM Operations
    async def clone_adom(
        self,
        source_adom: str,
        target_adom: str,
        description: str | None = None,
    ) -> ADOM:
        """Clone an ADOM with all its configurations.

        Args:
            source_adom: Source ADOM name to clone from
            target_adom: Target ADOM name to create
            description: Description for the new ADOM

        Returns:
            Cloned ADOM details
        """
        data = {
            "src-name": source_adom,
            "dst-name": target_adom,
        }
        if description:
            data["desc"] = description

        await self.client.execute("/dvmdb/adom/clone", data=data)
        return await self.get_adom(target_adom)

    async def move_device_to_adom(
        self,
        device_name: str,
        target_adom: str,
        source_adom: str = "root",
    ) -> None:
        """Move a device from one ADOM to another.

        Args:
            device_name: Device name to move
            target_adom: Target ADOM name
            source_adom: Source ADOM name (default: root)
        """
        data = {
            "device": device_name,
            "src-adom": source_adom,
            "dst-adom": target_adom,
        }
        await self.client.execute("/dvm/cmd/move/device", data=data)

    async def move_vdom_to_adom(
        self,
        device_name: str,
        vdom_name: str,
        target_adom: str,
        source_adom: str = "root",
    ) -> None:
        """Move a VDOM from one ADOM to another.

        Args:
            device_name: Device name containing the VDOM
            vdom_name: VDOM name to move
            target_adom: Target ADOM name
            source_adom: Source ADOM name (default: root)
        """
        data = {
            "device": device_name,
            "vdom": vdom_name,
            "src-adom": source_adom,
            "dst-adom": target_adom,
        }
        await self.client.execute("/dvm/cmd/move/vdom", data=data)

    async def get_adom_revision_list(
        self,
        adom: str,
    ) -> list[dict[str, Any]]:
        """Get ADOM revision history.

        Args:
            adom: ADOM name

        Returns:
            List of ADOM revisions
        """
        url = f"/dvmdb/adom/{adom}/revision"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def revert_adom_revision(
        self,
        adom: str,
        revision_id: int,
    ) -> None:
        """Revert ADOM to a specific revision.

        Args:
            adom: ADOM name
            revision_id: Revision ID to revert to
        """
        data = {
            "adom": adom,
            "version": revision_id,
        }
        await self.client.execute("/dvmdb/adom/revision/revert", data=data)

    async def create_adom_revision(
        self,
        adom: str,
        name: str,
        description: str | None = None,
        locked: bool = False,
    ) -> dict[str, Any]:
        """Create a manual ADOM revision/checkpoint.

        Args:
            adom: ADOM name
            name: Revision name
            description: Revision description
            locked: Lock revision to prevent auto-deletion

        Returns:
            Created revision information
        """
        data = {
            "name": name,
            "locked": 1 if locked else 0,
        }
        if description:
            data["desc"] = description

        url = f"/dvmdb/adom/{adom}/revision"
        await self.client.add(url, data=data)
        return {"name": name, "adom": adom}

    async def delete_adom_revision(
        self,
        adom: str,
        revision_id: int,
    ) -> None:
        """Delete an ADOM revision.

        Args:
            adom: ADOM name
            revision_id: Revision ID to delete
        """
        url = f"/dvmdb/adom/{adom}/revision/{revision_id}"
        await self.client.delete(url)

    async def get_adom_checksum(
        self,
        adom: str,
    ) -> dict[str, Any]:
        """Get ADOM configuration checksum.

        Args:
            adom: ADOM name

        Returns:
            Checksum information
        """
        data = {"adom": adom}
        result = await self.client.execute("/dvmdb/adom/checksum", data=data)
        return result

    async def check_adom_integrity(
        self,
        adom: str,
    ) -> dict[str, Any]:
        """Check ADOM database integrity.

        Args:
            adom: ADOM name

        Returns:
            Integrity check results
        """
        data = {"adom": adom}
        result = await self.client.execute("/dvm/cmd/check-integrity", data=data)
        return result

    async def upgrade_adom(
        self,
        adom: str,
        target_version: str,
        target_mr: int = 0,
    ) -> dict[str, Any]:
        """Upgrade ADOM to a different FortiOS version.

        Args:
            adom: ADOM name
            target_version: Target FortiOS version (e.g., "7.2")
            target_mr: Target maintenance release

        Returns:
            Upgrade task information
        """
        data = {
            "adom": adom,
            "target-ver": target_version,
            "target-mr": target_mr,
        }
        result = await self.client.execute("/dvmdb/adom/upgrade", data=data)
        return result

    async def get_adom_where_used(
        self,
        adom: str,
        object_type: str,
        object_name: str,
    ) -> list[dict[str, Any]]:
        """Get where an object is used within an ADOM.

        Args:
            adom: ADOM name
            object_type: Object type (e.g., "firewall address")
            object_name: Object name

        Returns:
            List of locations where object is used
        """
        data = {
            "adom": adom,
            "mkey": object_name,
        }
        url = f"/pm/config/adom/{adom}/obj/{object_type.replace(' ', '/')}/where-used"
        result = await self.client.execute(url, data=data)
        return result if isinstance(result, list) else [result] if result else []

    async def get_adom_object_usage(
        self,
        adom: str,
    ) -> dict[str, Any]:
        """Get ADOM object usage statistics.

        Args:
            adom: ADOM name

        Returns:
            Object usage statistics
        """
        url = f"/dvmdb/adom/{adom}/object-usage"
        result = await self.client.get(url)
        return result

    async def assign_device_to_adom(
        self,
        device_name: str,
        adom: str,
        vdom: str = "root",
    ) -> None:
        """Assign a device/VDOM to an ADOM.

        Args:
            device_name: Device name
            adom: Target ADOM name
            vdom: VDOM name (default: root)
        """
        # Update device to set its ADOM
        device_url = f"/dvmdb/device/{device_name}/vdom/{vdom}"
        data = {"adm-usr": adom}
        await self.client.set(device_url, data=data)

    # =========================================================================
    # Phase 28: Complete ADOM Management
    # =========================================================================

    async def lock_adom(
        self,
        adom: str,
    ) -> dict[str, Any]:
        """Lock ADOM workspace for exclusive editing.

        Locks prevent other administrators from making concurrent
        changes to the ADOM configuration.

        Args:
            adom: ADOM name to lock

        Returns:
            Lock status
        """
        url = f"/dvmdb/adom/{adom}/workspace/lock"
        return await self.client.exec(url, data={})

    async def unlock_adom(
        self,
        adom: str,
    ) -> dict[str, Any]:
        """Unlock ADOM workspace.

        Releases the workspace lock to allow other administrators
        to make changes.

        Args:
            adom: ADOM name to unlock

        Returns:
            Unlock status
        """
        url = f"/dvmdb/adom/{adom}/workspace/unlock"
        return await self.client.exec(url, data={})

    async def get_adom_policy_sync_status(
        self,
        adom: str,
    ) -> dict[str, Any]:
        """Get ADOM policy synchronization status.

        Shows sync status between ADOM database and managed devices.

        Args:
            adom: ADOM name

        Returns:
            Policy sync status
        """
        url = f"/dvmdb/adom/{adom}/sync/status"
        return await self.client.get(url)

    async def get_adom_meta_fields(
        self,
        adom: str,
    ) -> list[dict[str, Any]]:
        """Get ADOM metadata fields and values.

        Metadata fields are custom key-value pairs for categorizing
        and tagging ADOMs.

        Args:
            adom: ADOM name

        Returns:
            List of metadata fields
        """
        url = f"/dvmdb/adom/{adom}/meta-fields"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    # =========================================================================
    # Phase 43: Complete ADOM Operations
    # =========================================================================

    async def get_adom_statistics(
        self,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get comprehensive statistics for an ADOM.

        Args:
            adom: ADOM name

        Returns:
            ADOM statistics including devices, policies, objects count

        Note:
            This endpoint may not be available in all FortiManager versions.
        """
        try:
            url = f"/dvmdb/adom/{adom}/statistics"
            data = await self.client.get(url)
            return data if isinstance(data, dict) else {}
        except ResourceNotFoundError as e:
            return {
                "error": "ADOM statistics endpoint not supported",
                "message": "This FortiManager version does not support the ADOM statistics endpoint",
                "adom": adom,
                "supported_alternatives": ["get_adom_object_statistics", "get_adom_policy_statistics"]
            }
        except Exception as e:
            raise

    async def export_adom_configuration(
        self,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Export ADOM configuration for backup.
        
        Args:
            adom: ADOM name
            
        Returns:
            Exported configuration
        """
        url = f"/pm/config/adom/{adom}/export"
        return await self.client.execute(url, {})

    async def get_adom_health_status(
        self,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get health status of ADOM including all devices.

        Args:
            adom: ADOM name

        Returns:
            Health status information

        Note:
            This endpoint may not be available in all FortiManager versions.
        """
        try:
            url = f"/dvmdb/adom/{adom}/health"
            data = await self.client.get(url)
            return data if isinstance(data, dict) else {}
        except ResourceNotFoundError as e:
            return {
                "error": "ADOM health endpoint not supported",
                "message": "This FortiManager version does not support the ADOM health status endpoint",
                "adom": adom,
                "note": "Use device-specific health checks or system status instead"
            }
        except Exception as e:
            raise

    async def get_adom_disk_usage(
        self,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get disk usage statistics for ADOM data.

        Args:
            adom: ADOM name

        Returns:
            Disk usage information

        Note:
            This endpoint may not be available in all FortiManager versions.
        """
        try:
            url = f"/dvmdb/adom/{adom}/disk-usage"
            data = await self.client.get(url)
            return data if isinstance(data, dict) else {}
        except ResourceNotFoundError as e:
            return {
                "error": "ADOM disk usage endpoint not supported",
                "message": "This FortiManager version does not support the ADOM disk usage endpoint",
                "adom": adom,
                "note": "Disk usage information may be available through system-level monitoring"
            }
        except Exception as e:
            raise

    async def list_adom_templates(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List all templates in an ADOM.
        
        Args:
            adom: ADOM name
            
        Returns:
            List of templates
        """
        url = f"/pm/config/adom/{adom}/obj/cli/template-group"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def get_adom_object_count(
        self,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get count of all objects in an ADOM.
        
        Args:
            adom: ADOM name
            
        Returns:
            Object count statistics
        """
        url = f"/pm/config/adom/{adom}/_data/stats/obj"
        return await self.client.get(url)

    async def get_adom_policy_count(
        self,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get count of all policies in an ADOM.
        
        Args:
            adom: ADOM name
            
        Returns:
            Policy count statistics
        """
        url = f"/pm/config/adom/{adom}/_data/stats/pkg"
        return await self.client.get(url)

    # =========================================================================
    # Phase 46: ADOM Advanced Operations
    # =========================================================================

    async def create_adom_advanced(
        self,
        name: str,
        os_version: str,
        description: str = "",
        maintenance_release: int = 0,
        enable_central_management: bool = True,
        enable_split_task: bool = True,
        restricted_products: list[str] | None = None,
    ) -> dict[str, Any]:
        """Create ADOM with advanced configuration options.
        
        Allows fine-grained control over ADOM creation including OS version,
        maintenance release, management flags, and product restrictions.
        
        Args:
            name: ADOM name
            os_version: FortiOS version (e.g., "6.0", "7.0", "7.2", "7.4")
            description: ADOM description
            maintenance_release: Maintenance release number (e.g., 13 for 7.0.13)
            enable_central_management: Enable central management flag
            enable_split_task: Enable split task processing
            restricted_products: Product restrictions (e.g., ["fos", "fml"])
            
        Returns:
            Created ADOM details
            
        Example:
            create_adom_advanced(
                name="production-adom",
                os_version="7.4",
                maintenance_release=8,
                description="Production environment with FOS 7.4.8",
                restricted_products=["fos"]
            )
        """
        # Build flags from boolean options
        flags = 0
        if enable_central_management:
            flags |= 2048  # 0x800: Central Management
        if enable_split_task:
            flags |= 8  # 0x8: Split Task
        
        data = {
            "name": name,
            "desc": description,
            "os_ver": os_version,
            "mr": maintenance_release,
            "flags": flags,
            "state": 1,  # 1=enabled
        }
        
        if restricted_products:
            data["restricted_prds"] = restricted_products
        
        url = "/dvmdb/adom"
        return await self.client.add(url, data=data)

    async def create_adom_with_devices(
        self,
        name: str,
        os_version: str,
        devices: list[dict[str, str]],
        description: str = "",
    ) -> dict[str, Any]:
        """Create ADOM and assign devices in one atomic operation.
        
        Creates a new ADOM and moves specified devices to it. This is more
        efficient than creating the ADOM and then moving devices separately.
        
        Args:
            name: ADOM name
            os_version: FortiOS version
            devices: List of device assignments [{"name": "device", "vdom": "vdom"}]
            description: ADOM description
            
        Returns:
            Created ADOM with device assignments
            
        Example:
            create_adom_with_devices(
                name="branch-offices",
                os_version="7.2",
                devices=[
                    {"name": "FGT-BRANCH-01", "vdom": "root"},
                    {"name": "FGT-BRANCH-02", "vdom": "root"}
                ],
                description="Branch office devices"
            )
            
        Note:
            Devices must exist and be in a state that allows ADOM assignment.
        """
        data = {
            "name": name,
            "desc": description,
            "os_ver": os_version,
            "device_member": devices,
            "state": 1,
        }
        
        url = "/dvmdb/adom"
        return await self.client.add(url, data=data)

    async def get_adom_display_preferences(self) -> dict[str, Any]:
        """Get ADOM display and selection preferences from FortiManager.
        
        Retrieves system-level settings that control how ADOMs are displayed
        and selected in the FortiManager interface and API.
        
        Returns:
            ADOM display configuration including:
            - adom_enabled: Whether ADOM mode is enabled
            - adom_select_mode: "auto" or "manual" selection
            - raw: Complete system configuration
            
        Example Response:
            {
                "adom_enabled": True,
                "adom_select_mode": "auto",
                "raw": {...}
            }
        """
        url = "/cli/global/system/global"
        data = await self.client.get(url)
        
        # Extract and format ADOM-related fields
        return {
            "adom_enabled": data.get("adom-status", 0) == 1,
            "adom_select_mode": "manual" if data.get("adom-select", 0) == 1 else "auto",
            "raw": data,
        }

    async def get_adom_resource_limits(
        self,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get ADOM resource limits and current usage.
        
        Retrieves capacity limits and current resource utilization for an ADOM,
        useful for capacity planning and monitoring.
        
        Args:
            adom: ADOM name
            
        Returns:
            Resource limits including:
            - max_devices: Maximum number of devices
            - max_policies: Maximum number of policies  
            - max_objects: Maximum number of objects
            - workspace_mode: Workspace mode (normal, advanced, etc.)
            - state: ADOM state
            
        Example Response:
            {
                "max_devices": 1000,
                "max_policies": 10000,
                "max_objects": 50000,
                "workspace_mode": 1,
                "state": 1
            }
        """
        url = f"/dvmdb/adom/{adom}"
        data = await self.client.get(url)
        
        return {
            "adom": adom,
            "max_devices": data.get("max-devices", 0),
            "max_policies": data.get("max-policies", 0),
            "max_objects": data.get("max-objects", 0),
            "workspace_mode": data.get("workspace-mode", 0),
            "state": data.get("state", 0),
            "os_version": data.get("os_ver", ""),
            "limits": data,
        }

