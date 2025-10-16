"""Device management API module."""

from typing import Any

from fortimanager_mcp.api.client import FortiManagerClient
from fortimanager_mcp.api.models import Device


class DeviceAPI:
    """Device management operations."""

    def __init__(self, client: FortiManagerClient) -> None:
        """Initialize device API.

        Args:
            client: FortiManager client instance
        """
        self.client = client

    async def list_devices(
        self,
        adom: str | None = None,
        fields: list[str] | None = None,
        filter: list[Any] | None = None,
    ) -> list[Device]:
        """List all managed devices.

        Args:
            adom: ADOM to filter devices (None for all ADOMs)
            fields: Specific fields to return
            filter: Filter criteria

        Returns:
            List of devices
        """
        url = "/dvmdb/adom/{adom}/device" if adom else "/dvmdb/device"
        if adom:
            url = url.format(adom=adom)

        data = await self.client.get(url, fields=fields, filter=filter)
        if not isinstance(data, list):
            data = [data] if data else []

        return [Device(**item) for item in data]

    async def get_device(self, name: str, adom: str | None = None) -> Device:
        """Get specific device details.

        Args:
            name: Device name
            adom: ADOM name

        Returns:
            Device details
        """
        url = f"/dvmdb/adom/{adom}/device/{name}" if adom else f"/dvmdb/device/{name}"
        data = await self.client.get(url)
        return Device(**data)

    async def add_device(
        self,
        name: str,
        ip: str,
        username: str,
        password: str,
        adom: str = "root",
        **kwargs: Any,
    ) -> Device:
        """Add new managed device.

        Args:
            name: Device name
            ip: Device IP address
            username: Device admin username
            password: Device admin password
            adom: ADOM to add device to
            **kwargs: Additional device parameters

        Returns:
            Created device
        """
        data = {
            "device action": "add_model",
            "adom": adom,
            "device": {
                "name": name,
                "ip": ip,
                "adm_usr": username,
                "adm_pass": password,
                **kwargs,
            },
            "flags": ["create_task"],
        }

        result = await self.client.execute("/dvm/cmd/add/device", data=data)
        return await self.get_device(name, adom=adom)

    async def delete_device(self, name: str, adom: str = "root") -> None:
        """Delete managed device.

        Args:
            name: Device name
            adom: ADOM name
        """
        data = {
            "device": name,
            "adom": adom,
            "flags": ["create_task"],
        }
        await self.client.execute("/dvm/cmd/del/device", data=data)

    async def get_device_config(
        self,
        device: str,
        scope: str,
        path: str,
        vdom: str | None = None,
    ) -> Any:
        """Get device configuration.

        Args:
            device: Device name
            scope: Configuration scope (global or vdom)
            path: Configuration path (e.g., system/dns)
            vdom: VDOM name (required for vdom scope)

        Returns:
            Configuration data
        """
        if scope == "global":
            url = f"/pm/config/device/{device}/global/{path}"
        elif scope == "vdom":
            if not vdom:
                raise ValueError("VDOM name required for vdom scope")
            url = f"/pm/config/device/{device}/vdom/{vdom}/{path}"
        else:
            raise ValueError("Scope must be 'global' or 'vdom'")

        return await self.client.get(url)

    async def set_device_config(
        self,
        device: str,
        scope: str,
        path: str,
        data: dict[str, Any],
        vdom: str | None = None,
    ) -> Any:
        """Set device configuration.

        Args:
            device: Device name
            scope: Configuration scope (global or vdom)
            path: Configuration path
            data: Configuration data
            vdom: VDOM name (required for vdom scope)

        Returns:
            Update result
        """
        if scope == "global":
            url = f"/pm/config/device/{device}/global/{path}"
        elif scope == "vdom":
            if not vdom:
                raise ValueError("VDOM name required for vdom scope")
            url = f"/pm/config/device/{device}/vdom/{vdom}/{path}"
        else:
            raise ValueError("Scope must be 'global' or 'vdom'")

        return await self.client.set(url, data=data)

    async def install_device_settings(
        self,
        device: str,
        adom: str = "root",
        vdom: str = "root",
        comments: str | None = None,
    ) -> dict[str, Any]:
        """Install pending device settings.

        Args:
            device: Device name
            adom: ADOM name
            vdom: VDOM name
            comments: Installation comments

        Returns:
            Installation task information
        """
        data = {
            "adom": adom,
            "scope": [{"name": device, "vdom": vdom}],
            "flags": ["none"],
        }

        if comments:
            data["dev_rev_comments"] = comments

        return await self.client.execute("/securityconsole/install/device", data=data)

    # ============================================================================
    # Phase 1: Basic Device Operations (NEW)
    # ============================================================================

    async def add_real_device(
        self,
        name: str,
        ip: str,
        username: str,
        password: str,
        adom: str = "root",
        mgmt_mode: str = "fmg",
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Add a real (physical) FortiGate device.

        Args:
            name: Device name
            ip: Device IP address
            username: Admin username
            password: Admin password
            adom: ADOM to add device to
            mgmt_mode: Management mode (fmg, fmgfaz, unreg)
            **kwargs: Additional device parameters

        Returns:
            Task information
        """
        data = {
            "adom": adom,
            "device": {
                "name": name,
                "ip": ip,
                "adm_usr": username,
                "adm_pass": password,
                "mgmt_mode": mgmt_mode,
                **kwargs,
            },
            "flags": ["create_task", "nonblocking"],
        }
        return await self.client.exec("/dvm/cmd/add/device", data=data)

    async def rename_device(
        self,
        current_name: str,
        new_name: str,
        adom: str | None = None,
    ) -> dict[str, Any]:
        """Rename a managed device.

        Args:
            current_name: Current device name
            new_name: New device name
            adom: ADOM name (None for global)

        Returns:
            Update result
        """
        url = f"/dvmdb/adom/{adom}/device/{current_name}" if adom else f"/dvmdb/device/{current_name}"
        data = {"name": new_name}
        return await self.client.update(url, data=data)

    async def refresh_device(
        self,
        device: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Refresh device configuration from the managed device.

        Args:
            device: Device name
            adom: ADOM name

        Returns:
            Task information
        """
        data = {
            "adom": adom,
            "device": device,
            "flags": ["create_task", "nonblocking"],
        }
        return await self.client.exec("/dvm/cmd/update/device", data=data)

    async def get_device_oid(
        self,
        device_name: str,
    ) -> int:
        """Get the OID (Object ID) of a managed device.

        Args:
            device_name: Device name

        Returns:
            Device OID
        """
        devices = await self.client.get(
            "/dvmdb/device",
            fields=["name", "oid"],
            filter=["name", "==", device_name],
            options=["no loadsub"],
        )
        if not devices:
            raise ValueError(f"Device '{device_name}' not found")
        device_list = devices if isinstance(devices, list) else [devices]
        return device_list[0].get("oid")

    async def get_unauthorized_devices(self) -> list[dict[str, Any]]:
        """Get list of unauthorized (unregistered) devices.

        Returns:
            List of unauthorized devices
        """
        data = await self.client.get(
            "/dvmdb/device",
            fields=["name", "mgmt_mode", "ip", "sn", "platform_str"],
            filter=["mgmt_mode", "==", "unreg"],
            loadsub=0,
        )
        return data if isinstance(data, list) else [data] if data else []

    async def authorize_device(
        self,
        device_name: str,
        username: str | None = None,
        password: str | None = None,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Promote/authorize an unauthorized device.

        Args:
            device_name: Device name
            username: Admin username (optional if already configured)
            password: Admin password (optional if already configured)
            adom: ADOM to add device to

        Returns:
            Task information
        """
        device_data: dict[str, Any] = {
            "name": device_name,
            "device action": "promote_unreg",
        }

        if username and password:
            device_data["adm_usr"] = username
            device_data["adm_pass"] = password

        data = {
            "adom": adom,
            "device": device_data,
            "flags": ["create_task", "nonblocking"],
        }
        return await self.client.exec("/dvm/cmd/add/device", data=data)

    async def change_device_serial_number(
        self,
        device_name: str,
        new_serial_number: str,
    ) -> dict[str, Any]:
        """Change the serial number of a managed device.

        Args:
            device_name: Device name
            new_serial_number: New serial number

        Returns:
            Update result
        """
        url = f"/dvmdb/device/replace/sn/{device_name}"
        data = {"sn": new_serial_number}
        return await self.client.update(url, data=data)

    async def get_available_timezones(self) -> list[dict[str, Any]]:
        """Get list of available timezones for devices.

        Returns:
            List of timezones
        """
        data = await self.client.get("/cli/global/system/global?datasrc=device&option=timezone")
        return data if isinstance(data, list) else [data] if data else []

    async def get_full_device_db_syntax(self, adom: str = "root") -> dict[str, Any]:
        """Get the full device database syntax/schema.

        Args:
            adom: ADOM name

        Returns:
            Device database syntax
        """
        return await self.client.get(f"/pm/config/adom/{adom}/_data/dvmdb")

    # ============================================================================
    # Phase 2: Model Devices (NEW)
    # ============================================================================

    async def get_supported_model_devices(self) -> list[dict[str, Any]]:
        """Get list of supported model device platforms.

        Returns:
            List of supported platforms
        """
        data = await self.client.get("/dvmdb/_data/device/platform")
        return data if isinstance(data, list) else [data] if data else []

    async def create_model_device(
        self,
        name: str,
        platform: str,
        serial_number: str,
        adom: str = "root",
        os_ver: str = "7.0",
        mr: int = 0,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Create a model (virtual) device.

        Args:
            name: Device name
            platform: Platform string (e.g., "FortiGate-VM64")
            serial_number: Serial number for the model device
            adom: ADOM to add device to
            os_ver: OS version
            mr: Maintenance release
            **kwargs: Additional parameters

        Returns:
            Task information
        """
        data = {
            "adom": adom,
            "device": {
                "name": name,
                "device action": "add_model",
                "platform_str": platform,
                "sn": serial_number,
                "os_type": "fos",
                "os_ver": os_ver,
                "mr": mr,
                "mgmt_mode": "fmg",
                **kwargs,
            },
            "flags": ["create_task", "nonblocking"],
        }
        return await self.client.exec("/dvm/cmd/add/device", data=data)

    async def list_model_devices(self, adom: str | None = None) -> list[dict[str, Any]]:
        """List model devices (filter by flags).

        Args:
            adom: Optional ADOM name

        Returns:
            List of model devices
        """
        url = f"/dvmdb/adom/{adom}/device" if adom else "/dvmdb/device"
        # Model devices have specific flags set
        data = await self.client.get(
            url,
            fields=["name", "sn", "flags", "platform_str", "os_ver"],
            loadsub=0,
        )
        return data if isinstance(data, list) else [data] if data else []

    async def enable_device_auto_link(
        self,
        device_name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Enable auto-link flag on a model device.

        Args:
            device_name: Device name
            adom: ADOM name

        Returns:
            Update result
        """
        # Get current flags
        url = f"/dvmdb/adom/{adom}/device/{device_name}"
        device = await self.client.get(url, fields=["flags"])
        
        flags = device.get("flags", [])
        if "auto_link" not in flags:
            flags.append("auto_link")
        
        return await self.client.update(url, data={"flags": flags})

    async def disable_device_auto_link(
        self,
        device_name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Disable auto-link flag on a model device.

        Args:
            device_name: Device name
            adom: ADOM name

        Returns:
            Update result
        """
        url = f"/dvmdb/adom/{adom}/device/{device_name}"
        device = await self.client.get(url, fields=["flags"])
        
        flags = device.get("flags", [])
        if "auto_link" in flags:
            flags.remove("auto_link")
        
        return await self.client.update(url, data={"flags": flags})

    # ============================================================================
    # Phase 3: Device Groups (NEW)
    # ============================================================================

    async def create_device_group(
        self,
        name: str,
        adom: str = "root",
        description: str | None = None,
    ) -> dict[str, Any]:
        """Create a device group.

        Args:
            name: Group name
            adom: ADOM name
            description: Optional description

        Returns:
            Created group
        """
        data: dict[str, Any] = {"name": name}
        if description:
            data["desc"] = description
        
        url = f"/dvmdb/adom/{adom}/group"
        return await self.client.add(url, data=data)

    async def list_device_groups(self, adom: str = "root") -> list[dict[str, Any]]:
        """List device groups.

        Args:
            adom: ADOM name

        Returns:
            List of device groups
        """
        url = f"/dvmdb/adom/{adom}/group"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def get_device_group(
        self,
        group_name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get device group details.

        Args:
            group_name: Group name
            adom: ADOM name

        Returns:
            Group details
        """
        url = f"/dvmdb/adom/{adom}/group/{group_name}"
        return await self.client.get(url)

    async def add_device_to_group(
        self,
        device_name: str,
        group_name: str,
        adom: str = "root",
        vdom: str = "root",
    ) -> dict[str, Any]:
        """Add a device to a device group.

        Args:
            device_name: Device name
            group_name: Group name
            adom: ADOM name
            vdom: VDOM name

        Returns:
            Update result
        """
        url = f"/dvmdb/adom/{adom}/group/{group_name}/object member"
        data = {"name": device_name, "vdom": vdom}
        return await self.client.add(url, data=data)

    async def remove_device_from_group(
        self,
        device_name: str,
        group_name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Remove a device from a device group.

        Args:
            device_name: Device name
            group_name: Group name
            adom: ADOM name

        Returns:
            Delete result
        """
        url = f"/dvmdb/adom/{adom}/group/{group_name}/object member/{device_name}"
        return await self.client.delete(url)

    async def delete_device_group(
        self,
        group_name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Delete a device group.

        Args:
            group_name: Group name
            adom: ADOM name

        Returns:
            Delete result
        """
        url = f"/dvmdb/adom/{adom}/group/{group_name}"
        return await self.client.delete(url)

    async def get_device_group_members(
        self,
        group_name: str,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """Get members of a device group.

        Args:
            group_name: Group name
            adom: ADOM name

        Returns:
            List of group members
        """
        url = f"/dvmdb/adom/{adom}/group/{group_name}/object member"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    # ============================================================================
    # Phase 4: VDOM Operations (NEW)
    # ============================================================================

    async def enable_vdom(
        self,
        device_name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Enable VDOM mode on a device.

        Args:
            device_name: Device name
            adom: ADOM name

        Returns:
            Update result
        """
        url = f"/pm/config/device/{device_name}/global/system/global"
        data = {"vdom-mode": "multi-vdom"}
        return await self.client.update(url, data=data)

    async def add_vdom(
        self,
        device_name: str,
        vdom_name: str,
        adom: str = "root",
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Add a VDOM to a device.

        Args:
            device_name: Device name
            vdom_name: VDOM name
            adom: ADOM name
            **kwargs: Additional VDOM parameters

        Returns:
            Created VDOM
        """
        url = f"/pm/config/device/{device_name}/global/system/vdom"
        data = {"name": vdom_name, **kwargs}
        return await self.client.add(url, data=data)

    async def delete_vdom(
        self,
        device_name: str,
        vdom_name: str,
    ) -> dict[str, Any]:
        """Delete a VDOM from a device.

        Args:
            device_name: Device name
            vdom_name: VDOM name

        Returns:
            Delete result
        """
        url = f"/pm/config/device/{device_name}/global/system/vdom/{vdom_name}"
        return await self.client.delete(url)

    async def list_device_vdoms(
        self,
        device_name: str,
        adom: str | None = None,
    ) -> list[dict[str, Any]]:
        """List VDOMs for a device.

        Args:
            device_name: Device name
            adom: Optional ADOM name

        Returns:
            List of VDOMs
        """
        url = f"/dvmdb/adom/{adom}/device/{device_name}" if adom else f"/dvmdb/device/{device_name}"
        device = await self.client.get(url, fields=["vdom"])
        vdoms = device.get("vdom", [])
        return vdoms if isinstance(vdoms, list) else [vdoms] if vdoms else []

    async def assign_vdom_to_adom(
        self,
        device_name: str,
        vdom_name: str,
        target_adom: str,
        source_adom: str = "root",
    ) -> dict[str, Any]:
        """Assign a VDOM to an ADOM.

        Args:
            device_name: Device name
            vdom_name: VDOM name
            target_adom: Target ADOM to assign to
            source_adom: Source ADOM

        Returns:
            Assignment result
        """
        data = {
            "device": device_name,
            "vdom": vdom_name,
            "source-adom": source_adom,
            "target-adom": target_adom,
        }
        return await self.client.exec("/dvmdb/adom/assign", data=data)

    # ============================================================================
    # Phase 5: Firmware Management (NEW)
    # ============================================================================

    async def get_upgrade_path(
        self,
        device_name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get the upgrade path for a device.

        Args:
            device_name: Device name
            adom: ADOM name

        Returns:
            Upgrade path information
        """
        data = {
            "device": device_name,
            "adom": adom,
        }
        return await self.client.exec("/um/image/upgrade/ext", data=data)

    async def list_available_firmware(
        self,
        platform: str | None = None,
    ) -> list[dict[str, Any]]:
        """List firmware images available on FortiManager.

        Args:
            platform: Optional platform filter (e.g., "FortiGate-VM64")

        Returns:
            List of available firmware images
        """
        url = "/um/image/list" if not platform else f"/um/image/list?product={platform}"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def upgrade_device(
        self,
        device_name: str,
        image: str,
        adom: str = "root",
        create_task: bool = True,
    ) -> dict[str, Any]:
        """Upgrade a device to a specific firmware version.

        Args:
            device_name: Device name
            image: Firmware image path
            adom: ADOM name
            create_task: Whether to create a task

        Returns:
            Upgrade task information
        """
        data = {
            "adom": adom,
            "device": device_name,
            "image": image,
            "flags": ["create_task"] if create_task else [],
        }
        return await self.client.exec("/um/image/upgrade", data=data)

    async def get_upgrade_history(
        self,
        device_name: str | None = None,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """Get firmware upgrade history.

        Args:
            device_name: Optional device name filter
            adom: ADOM name

        Returns:
            List of upgrade history entries
        """
        url = "/um/image/upgrade/history"
        filter_param = [["device", "==", device_name]] if device_name else None
        data = await self.client.get(url, filter=filter_param)
        return data if isinstance(data, list) else [data] if data else []

    # ============================================================================
    # Phase 6: Device Revisions (NEW)
    # ============================================================================

    async def list_device_revisions(
        self,
        device_name: str,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List device configuration revisions.

        Args:
            device_name: Device name
            adom: ADOM name

        Returns:
            List of device revisions
        """
        url = f"/dvmdb/adom/{adom}/device/{device_name}/config/revision"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def get_device_revision(
        self,
        device_name: str,
        revision_id: int,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get a specific device configuration revision.

        Args:
            device_name: Device name
            revision_id: Revision ID
            adom: ADOM name

        Returns:
            Revision details
        """
        url = f"/dvmdb/adom/{adom}/device/{device_name}/config/revision/{revision_id}"
        return await self.client.get(url)

    async def get_current_device_config(
        self,
        device_name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get current device database configuration.

        Args:
            device_name: Device name
            adom: ADOM name

        Returns:
            Current device configuration
        """
        url = f"/dvmdb/adom/{adom}/device/{device_name}"
        return await self.client.get(url)

    async def revert_device_revision(
        self,
        device_name: str,
        revision_id: int,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Revert device to a specific configuration revision.

        Args:
            device_name: Device name
            revision_id: Revision ID to revert to
            adom: ADOM name

        Returns:
            Revert result
        """
        data = {
            "adom": adom,
            "device": device_name,
            "rev_id": revision_id,
        }
        return await self.client.exec("/dvmdb/device/config/revert", data=data)

    async def import_device_revision(
        self,
        device_name: str,
        revision_file: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Import a device configuration revision.

        Args:
            device_name: Device name
            revision_file: Path to revision file
            adom: ADOM name

        Returns:
            Import result
        """
        data = {
            "adom": adom,
            "device": device_name,
            "file": revision_file,
        }
        return await self.client.exec("/dvmdb/device/config/import", data=data)

    async def retrieve_device_config(
        self,
        device_name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Trigger a retrieve operation to get latest config from device.

        Args:
            device_name: Device name
            adom: ADOM name

        Returns:
            Task information
        """
        data = {
            "adom": adom,
            "device": device_name,
            "flags": ["create_task", "nonblocking"],
        }
        return await self.client.exec("/dvm/cmd/retrieve/device", data=data)

    # ============================================================================
    # Phase 7: HA Cluster Operations (NEW)
    # ============================================================================

    async def create_ha_cluster(
        self,
        name: str,
        platform: str,
        primary_sn: str,
        secondary_sn: str,
        adom: str = "root",
        os_ver: str = "7.0",
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Create a Model HA Cluster.

        Args:
            name: Cluster name
            platform: Platform string
            primary_sn: Primary device serial number
            secondary_sn: Secondary device serial number
            adom: ADOM name
            os_ver: OS version
            **kwargs: Additional cluster parameters

        Returns:
            Task information
        """
        data = {
            "adom": adom,
            "device": {
                "name": name,
                "device action": "add_model",
                "platform_str": platform,
                "sn": primary_sn,
                "os_type": "fos",
                "os_ver": os_ver,
                "mgmt_mode": "fmg",
                "ha_mode": "AP",  # Active-Passive
                "ha_slave": [
                    {
                        "idx": 1,
                        "name": f"{name}-secondary",
                        "prio": 1,
                        "role": "slave",
                        "sn": secondary_sn,
                    }
                ],
                **kwargs,
            },
            "flags": ["create_task", "nonblocking"],
        }
        return await self.client.exec("/dvm/cmd/add/device", data=data)

    async def get_cluster_members(
        self,
        cluster_name: str,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """Get HA cluster member information.

        Args:
            cluster_name: Cluster name
            adom: ADOM name

        Returns:
            List of cluster members
        """
        url = f"/dvmdb/adom/{adom}/device/{cluster_name}"
        device = await self.client.get(url, fields=["name", "ha_slave", "ha_mode"])
        slaves = device.get("ha_slave", [])
        return slaves if isinstance(slaves, list) else [slaves] if slaves else []

    async def failover_cluster(
        self,
        cluster_name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Trigger a failover for an HA cluster.

        Args:
            cluster_name: Cluster name
            adom: ADOM name

        Returns:
            Failover result
        """
        data = {
            "adom": adom,
            "device": cluster_name,
        }
        return await self.client.exec("/dvm/cmd/ha/failover", data=data)

    async def update_cluster_serial_numbers(
        self,
        cluster_name: str,
        primary_sn: str,
        secondary_sn: str | None = None,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Update/replace serial numbers of HA cluster members.

        Args:
            cluster_name: Cluster name
            primary_sn: New primary device serial number
            secondary_sn: New secondary device serial number
            adom: ADOM name

        Returns:
            Update result
        """
        url = f"/dvmdb/adom/{adom}/device/{cluster_name}"
        data: dict[str, Any] = {"sn": primary_sn}
        
        if secondary_sn:
            data["ha_slave"] = [
                {
                    "idx": 1,
                    "sn": secondary_sn,
                }
            ]
        
        return await self.client.update(url, data=data)

    async def get_cluster_status(
        self,
        cluster_name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get HA cluster members status.

        Args:
            cluster_name: Cluster name
            adom: ADOM name

        Returns:
            Cluster status information
        """
        url = f"/dvmdb/adom/{adom}/device/{cluster_name}"
        return await self.client.get(
            url,
            fields=["name", "ha_mode", "ha_slave", "conn_status", "is_connected"],
        )

    # ============================================================================
    # Phase 8: Device Metadata & Blueprints (NEW)
    # ============================================================================

    async def get_device_meta_fields(
        self,
        device_name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get device meta fields.

        Args:
            device_name: Device name
            adom: ADOM name

        Returns:
            Device meta fields
        """
        url = f"/dvmdb/adom/{adom}/device/{device_name}"
        device = await self.client.get(url, fields=["name", "meta fields"])
        return device.get("meta fields", {})

    async def set_device_meta_fields(
        self,
        device_name: str,
        meta_fields: dict[str, Any],
        adom: str = "root",
    ) -> dict[str, Any]:
        """Set device meta fields.

        Args:
            device_name: Device name
            meta_fields: Meta fields to set
            adom: ADOM name

        Returns:
            Update result
        """
        url = f"/dvmdb/adom/{adom}/device/{device_name}"
        return await self.client.update(url, data={"meta fields": meta_fields})

    async def get_vdom_meta_fields(
        self,
        device_name: str,
        vdom_name: str | None = None,
        adom: str = "root",
    ) -> dict[str, Any] | list[dict[str, Any]]:
        """Get VDOM meta fields for a device.

        Args:
            device_name: Device name
            vdom_name: Optional specific VDOM name (None for all VDOMs)
            adom: ADOM name

        Returns:
            VDOM meta fields
        """
        if vdom_name:
            url = f"/dvmdb/adom/{adom}/device/{device_name}/vdom/{vdom_name}"
            vdom = await self.client.get(url, fields=["name", "meta fields"])
            return vdom.get("meta fields", {})
        else:
            url = f"/dvmdb/adom/{adom}/device/{device_name}/vdom"
            vdoms = await self.client.get(url, fields=["name", "meta fields"])
            return vdoms if isinstance(vdoms, list) else [vdoms] if vdoms else []

    async def set_vdom_meta_fields(
        self,
        device_name: str,
        vdom_name: str,
        meta_fields: dict[str, Any],
        adom: str = "root",
    ) -> dict[str, Any]:
        """Set VDOM meta fields.

        Args:
            device_name: Device name
            vdom_name: VDOM name
            meta_fields: Meta fields to set
            adom: ADOM name

        Returns:
            Update result
        """
        url = f"/dvmdb/adom/{adom}/device/{device_name}/vdom/{vdom_name}"
        return await self.client.update(url, data={"meta fields": meta_fields})

    async def list_device_blueprints(self, adom: str = "root") -> list[dict[str, Any]]:
        """List device blueprints.

        Args:
            adom: ADOM name

        Returns:
            List of device blueprints
        """
        url = f"/pm/devprof/adom/{adom}"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def create_device_blueprint(
        self,
        name: str,
        adom: str = "root",
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Create a device blueprint.

        Args:
            name: Blueprint name
            adom: ADOM name
            **kwargs: Blueprint parameters

        Returns:
            Created blueprint
        """
        data = {"name": name, **kwargs}
        url = f"/pm/devprof/adom/{adom}"
        return await self.client.add(url, data=data)

    async def delete_device_blueprint(
        self,
        blueprint_name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Delete a device blueprint.

        Args:
            blueprint_name: Blueprint name
            adom: ADOM name

        Returns:
            Delete result
        """
        url = f"/pm/devprof/adom/{adom}/{blueprint_name}"
        return await self.client.delete(url)

    # ============================================================================
    # Phase 9: Network Settings (NEW)
    # ============================================================================

    async def add_vlan(
        self,
        device_name: str,
        interface: str,
        vlan_id: int,
        vdom: str = "root",
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Add a VLAN interface to a device.

        Args:
            device_name: Device name
            interface: Physical interface name
            vlan_id: VLAN ID
            vdom: VDOM name
            **kwargs: Additional VLAN parameters

        Returns:
            Created VLAN interface
        """
        vlan_name = f"{interface}.{vlan_id}"
        data = {
            "name": vlan_name,
            "interface": interface,
            "vlanid": vlan_id,
            "type": "vlan",
            **kwargs,
        }
        url = f"/pm/config/device/{device_name}/vdom/{vdom}/system/interface"
        return await self.client.add(url, data=data)

    async def add_zone_member(
        self,
        device_name: str,
        zone_name: str,
        interface: str,
        vdom: str = "root",
    ) -> dict[str, Any]:
        """Add an interface to a system zone.

        Args:
            device_name: Device name
            zone_name: Zone name
            interface: Interface to add
            vdom: VDOM name

        Returns:
            Update result
        """
        url = f"/pm/config/device/{device_name}/vdom/{vdom}/system/zone/{zone_name}"
        # Get current zone
        zone = await self.client.get(url)
        interfaces = zone.get("interface", [])
        if interface not in interfaces:
            interfaces.append(interface)
        return await self.client.update(url, data={"interface": interfaces})

    async def delete_zone_member(
        self,
        device_name: str,
        zone_name: str,
        interface: str,
        vdom: str = "root",
    ) -> dict[str, Any]:
        """Remove an interface from a system zone.

        Args:
            device_name: Device name
            zone_name: Zone name
            interface: Interface to remove
            vdom: VDOM name

        Returns:
            Update result
        """
        url = f"/pm/config/device/{device_name}/vdom/{vdom}/system/zone/{zone_name}"
        zone = await self.client.get(url)
        interfaces = zone.get("interface", [])
        if interface in interfaces:
            interfaces.remove(interface)
        return await self.client.update(url, data={"interface": interfaces})

    async def add_ospf_network(
        self,
        device_name: str,
        network: str,
        area: str,
        vdom: str = "root",
    ) -> dict[str, Any]:
        """Add OSPF network entry.

        Args:
            device_name: Device name
            network: Network address (e.g., "10.0.0.0 255.255.255.0")
            area: OSPF area ID
            vdom: VDOM name

        Returns:
            Created OSPF network
        """
        data = {
            "prefix": network,
            "area": area,
        }
        url = f"/pm/config/device/{device_name}/vdom/{vdom}/router/ospf/network"
        return await self.client.add(url, data=data)

    async def delete_ospf_network(
        self,
        device_name: str,
        network_id: int,
        vdom: str = "root",
    ) -> dict[str, Any]:
        """Delete OSPF network entry.

        Args:
            device_name: Device name
            network_id: Network entry ID
            vdom: VDOM name

        Returns:
            Delete result
        """
        url = f"/pm/config/device/{device_name}/vdom/{vdom}/router/ospf/network/{network_id}"
        return await self.client.delete(url)

    async def get_lte_modem_status(
        self,
        device_name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get LTE modem status for a device.

        Args:
            device_name: Device name
            adom: ADOM name

        Returns:
            LTE modem status
        """
        data = {
            "adom": adom,
            "device": device_name,
        }
        return await self.client.exec("/sys/proxy/json", data=data)

    # ============================================================================
    # Phase 10: Advanced Operations (NEW)
    # ============================================================================

    async def upload_certificate(
        self,
        device_name: str,
        cert_name: str,
        cert_content: str,
        vdom: str = "root",
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Upload a certificate to a device.

        Args:
            device_name: Device name
            cert_name: Certificate name
            cert_content: Certificate content (PEM format)
            vdom: VDOM name
            **kwargs: Additional certificate parameters

        Returns:
            Upload result
        """
        data = {
            "name": cert_name,
            "certificate": cert_content,
            **kwargs,
        }
        url = f"/pm/config/device/{device_name}/vdom/{vdom}/vpn.certificate/local"
        return await self.client.add(url, data=data)

    async def get_certificate_details(
        self,
        device_name: str,
        cert_name: str,
        vdom: str = "root",
    ) -> dict[str, Any]:
        """Get certificate details.

        Args:
            device_name: Device name
            cert_name: Certificate name
            vdom: VDOM name

        Returns:
            Certificate details
        """
        url = f"/pm/config/device/{device_name}/vdom/{vdom}/vpn.certificate/local/{cert_name}"
        return await self.client.get(url)

    async def get_install_preview(
        self,
        devices: list[str] | str,
        adom: str = "root",
        vdom: str = "root",
    ) -> dict[str, Any]:
        """Get install preview for device(s).

        Args:
            devices: Device name or list of device names
            adom: ADOM name
            vdom: VDOM name

        Returns:
            Install preview details
        """
        device_list = [devices] if isinstance(devices, str) else devices
        scope = [{"name": dev, "vdom": vdom} for dev in device_list]
        
        data = {
            "adom": adom,
            "scope": scope,
            "flags": ["preview"],
        }
        return await self.client.exec("/securityconsole/install/package", data=data)

    async def get_vpn_tunnel_details(
        self,
        device_name: str,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """Get VPN tunnel details/status.

        Args:
            device_name: Device name
            adom: ADOM name

        Returns:
            List of VPN tunnels
        """
        data = {
            "adom": adom,
            "device": device_name,
        }
        result = await self.client.exec("/sys/proxy/json", data=data)
        return result.get("tunnels", []) if isinstance(result, dict) else []

    async def set_rma_status(
        self,
        device_name: str,
        status: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Set RMA (Return Merchandise Authorization) status on a device.

        Args:
            device_name: Device name
            status: RMA status
            adom: ADOM name

        Returns:
            Update result
        """
        url = f"/dvmdb/adom/{adom}/device/{device_name}"
        return await self.client.update(url, data={"rma_status": status})

    async def get_rma_status(
        self,
        device_name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get RMA status of a device.

        Args:
            device_name: Device name
            adom: ADOM name

        Returns:
            RMA status
        """
        url = f"/dvmdb/adom/{adom}/device/{device_name}"
        device = await self.client.get(url, fields=["name", "rma_status"])
        return {"device": device_name, "rma_status": device.get("rma_status")}

    async def delete_rma_status(
        self,
        device_name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Delete RMA status from a device.

        Args:
            device_name: Device name
            adom: ADOM name

        Returns:
            Update result
        """
        url = f"/dvmdb/adom/{adom}/device/{device_name}"
        return await self.client.update(url, data={"rma_status": None})

    async def get_device_vulnerabilities(
        self,
        device_name: str | None = None,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """Get Fortinet vulnerabilities for managed devices.

        Args:
            device_name: Optional device name filter
            adom: ADOM name

        Returns:
            List of vulnerabilities
        """
        data = {
            "adom": adom,
        }
        if device_name:
            data["device"] = device_name
        
        result = await self.client.exec("/sys/status/vulnerabilities", data=data)
        return result if isinstance(result, list) else [result] if result else []

    async def run_cli_commands(
        self,
        device_name: str,
        commands: list[str],
        adom: str = "root",
    ) -> dict[str, Any]:
        """Run CLI commands against a managed device.

        Args:
            device_name: Device name
            commands: List of CLI commands to execute
            adom: ADOM name

        Returns:
            Command execution results
        """
        data = {
            "adom": adom,
            "device": device_name,
            "commands": commands,
        }
        return await self.client.exec("/sys/proxy/json", data=data)

    # =========================================================================
    # Phase 44: Additional Device Query Operations
    # =========================================================================

    async def get_device_ha_status(
        self,
        device_name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get device HA (High Availability) status.
        
        Args:
            device_name: Device name
            adom: ADOM name
            
        Returns:
            HA status information
        """
        url = f"/dvmdb/adom/{adom}/device/{device_name}/ha"
        return await self.client.get(url)

    async def get_device_interface_list(
        self,
        device_name: str,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """Get list of device interfaces.
        
        Args:
            device_name: Device name
            adom: ADOM name
            
        Returns:
            List of device interfaces
        """
        url = f"/dvmdb/adom/{adom}/device/{device_name}/vdom/root/interface"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def get_device_routing_table(
        self,
        device_name: str,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """Get device routing table.
        
        Args:
            device_name: Device name
            adom: ADOM name
            
        Returns:
            Routing table entries
        """
        url = f"/dvmdb/adom/{adom}/device/{device_name}/vdom/root/router/static"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def get_device_vpn_monitor(
        self,
        device_name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get device VPN tunnel monitoring information.
        
        Args:
            device_name: Device name
            adom: ADOM name
            
        Returns:
            VPN monitoring data
        """
        url = f"/dvmdb/adom/{adom}/device/{device_name}/vpn/monitor"
        return await self.client.get(url)

    async def get_device_system_status(
        self,
        device_name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get device system status details.
        
        Args:
            device_name: Device name
            adom: ADOM name
            
        Returns:
            System status information
        """
        url = f"/dvmdb/adom/{adom}/device/{device_name}/status"
        return await self.client.get(url)

