"""Installation operations API module."""

from typing import Any

from fortimanager_mcp.api.client import FortiManagerClient


class InstallationAPI:
    """Installation operations for device and policy package configurations."""

    def __init__(self, client: FortiManagerClient) -> None:
        """Initialize installation API.

        Args:
            client: FortiManager client instance
        """
        self.client = client

    async def install_device_settings(
        self,
        device: str,
        adom: str = "root",
        vdom: str = "root",
        comments: str | None = None,
        flags: list[str] | None = None,
    ) -> dict[str, Any]:
        """Install pending device settings (network & system).

        This installs only pending device settings changes.
        Security settings (objects, policies) are NOT installed.

        Args:
            device: Device name
            adom: ADOM name
            vdom: VDOM name
            comments: Installation comments
            flags: Installation flags

        Returns:
            Installation task information with task ID
        """
        data: dict[str, Any] = {
            "adom": adom,
            "scope": [{"name": device, "vdom": vdom}],
            "flags": flags or ["none"],
        }

        if comments:
            data["dev_rev_comments"] = comments

        result = await self.client.execute("/securityconsole/install/device", data=data)
        return result

    async def install_policy_package(
        self,
        package: str,
        device: str,
        adom: str = "root",
        vdom: str = "root",
        flags: list[str] | None = None,
    ) -> dict[str, Any]:
        """Install policy package to device.

        This installs both pending device settings AND pending security settings
        (objects and policies).

        Args:
            package: Policy package name
            device: Device name
            adom: ADOM name
            vdom: VDOM name
            flags: Installation flags

        Returns:
            Installation task information with task ID
        """
        data: dict[str, Any] = {
            "adom": adom,
            "pkg": package,
            "scope": [{"name": device, "vdom": vdom}],
            "flags": flags or ["none"],
        }

        result = await self.client.execute("/securityconsole/install/package", data=data)
        return result

    async def install_to_multiple_devices(
        self,
        package: str,
        devices: list[dict[str, str]],
        adom: str = "root",
        flags: list[str] | None = None,
    ) -> dict[str, Any]:
        """Install policy package to multiple devices.

        Args:
            package: Policy package name
            devices: List of devices [{"name": "device1", "vdom": "root"}, ...]
            adom: ADOM name
            flags: Installation flags

        Returns:
            Installation task information with task ID
        """
        data: dict[str, Any] = {
            "adom": adom,
            "pkg": package,
            "scope": devices,
            "flags": flags or ["none"],
        }

        result = await self.client.execute("/securityconsole/install/package", data=data)
        return result

    async def check_install_preview(
        self,
        package: str,
        device: str,
        adom: str = "root",
        vdom: str = "root",
    ) -> dict[str, Any]:
        """Preview policy package installation (dry run).

        Args:
            package: Policy package name
            device: Device name
            adom: ADOM name
            vdom: VDOM name

        Returns:
            Preview information
        """
        data = {
            "adom": adom,
            "pkg": package,
            "scope": [{"name": device, "vdom": vdom}],
            "flags": ["preview"],
        }

        result = await self.client.execute("/securityconsole/install/package", data=data)
        return result

    # Scheduled Installation Operations
    async def schedule_policy_install(
        self,
        package: str,
        device: str,
        schedule_time: str,
        adom: str = "root",
        vdom: str = "root",
    ) -> dict[str, Any]:
        """Schedule a policy package installation for later.

        Args:
            package: Policy package name
            device: Device name
            schedule_time: Scheduled time (format: "YYYY-MM-DD HH:MM:SS")
            adom: ADOM name
            vdom: VDOM name

        Returns:
            Scheduled installation task information
        """
        data = {
            "adom": adom,
            "pkg": package,
            "scope": [{"name": device, "vdom": vdom}],
            "schedule": schedule_time,
        }
        
        result = await self.client.execute("/securityconsole/install/package", data=data)
        return result

    async def list_scheduled_installs(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List scheduled policy package installations.

        Args:
            adom: ADOM name

        Returns:
            List of scheduled installations
        """
        url = f"/pm/config/adom/{adom}/obj/schedule/install"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def cancel_scheduled_install(
        self,
        schedule_id: int,
        adom: str = "root",
    ) -> None:
        """Cancel a scheduled policy package installation.

        Args:
            schedule_id: Scheduled installation ID
            adom: ADOM name
        """
        url = f"/pm/config/adom/{adom}/obj/schedule/install/{schedule_id}"
        await self.client.delete(url)

    # Advanced Install Preview Operations
    async def preview_install_multiple_devices(
        self,
        package: str,
        devices: list[dict[str, str]],
        adom: str = "root",
    ) -> dict[str, Any]:
        """Preview policy package installation on multiple devices.

        Args:
            package: Policy package name
            devices: List of devices [{"name": "device1", "vdom": "root"}, ...]
            adom: ADOM name

        Returns:
            Preview information for all devices
        """
        data = {
            "adom": adom,
            "pkg": package,
            "scope": devices,
            "flags": ["preview"],
        }
        
        result = await self.client.execute("/securityconsole/install/package", data=data)
        return result

    async def preview_partial_install(
        self,
        package: str,
        device: str,
        policy_ids: list[int],
        adom: str = "root",
        vdom: str = "root",
    ) -> dict[str, Any]:
        """Preview partial policy installation (specific policies only).

        Args:
            package: Policy package name
            device: Device name
            policy_ids: List of policy IDs to install
            adom: ADOM name
            vdom: VDOM name

        Returns:
            Preview information for partial install
        """
        data = {
            "adom": adom,
            "pkg": package,
            "scope": [{"name": device, "vdom": vdom}],
            "policyid": policy_ids,
            "flags": ["preview"],
        }
        
        result = await self.client.execute("/securityconsole/install/package", data=data)
        return result

    # =========================================================================
    # Phase 38: Advanced Installation Operations
    # =========================================================================

    async def abort_install(
        self,
        task_id: int,
    ) -> dict[str, Any]:
        """Abort an ongoing installation task.
        
        Args:
            task_id: Installation task ID
            
        Returns:
            Abort result
        """
        url = "/securityconsole/install/abort"
        data = {"id": task_id}
        return await self.client.execute(url, data)

    async def get_install_history(
        self,
        device: str,
        adom: str = "root",
        limit: int = 50,
    ) -> list[dict[str, Any]]:
        """Get installation history for a device.
        
        Args:
            device: Device name
            adom: ADOM name
            limit: Maximum records
            
        Returns:
            Installation history
        """
        url = f"/dvmdb/adom/{adom}/device/{device}/install/history"
        params = {"limit": limit}
        data = await self.client.get(url, **params)
        return data if isinstance(data, list) else [data] if data else []

    async def validate_install_package(
        self,
        package: str,
        adom: str = "root",
        devices: list[str] | None = None,
    ) -> dict[str, Any]:
        """Validate policy package before installation.
        
        Args:
            package: Package name
            adom: ADOM name
            devices: Device list (optional)
            
        Returns:
            Validation results
        """
        url = "/securityconsole/install/validate"
        data = {
            "adom": adom,
            "pkg": package,
        }
        if devices:
            data["scope"] = [{"name": dev} for dev in devices]
        return await self.client.execute(url, data)

    async def get_install_progress(
        self,
        task_id: int,
    ) -> dict[str, Any]:
        """Get real-time installation progress.
        
        Args:
            task_id: Installation task ID
            
        Returns:
            Progress information
        """
        url = f"/task/task/{task_id}/line"
        data = await self.client.get(url)
        return data if isinstance(data, dict) else {}

    async def schedule_install(
        self,
        package: str,
        devices: list[str],
        adom: str = "root",
        schedule_time: str | None = None,
    ) -> dict[str, Any]:
        """Schedule a policy package installation.
        
        Args:
            package: Package name
            devices: Device names
            adom: ADOM name
            schedule_time: ISO format time
            
        Returns:
            Schedule result
        """
        url = "/securityconsole/install/package"
        data = {
            "adom": adom,
            "pkg": package,
            "scope": [{"name": dev, "vdom": "root"} for dev in devices],
        }
        if schedule_time:
            data["schedule_time"] = schedule_time
        return await self.client.execute(url, data)

    async def cancel_scheduled_install(
        self,
        schedule_id: int,
    ) -> dict[str, Any]:
        """Cancel a scheduled installation.
        
        Args:
            schedule_id: Schedule ID
            
        Returns:
            Cancellation result
        """
        url = "/securityconsole/install/schedule/cancel"
        data = {"id": schedule_id}
        return await self.client.execute(url, data)

    async def get_device_install_targets(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """Get list of devices available for installation.
        
        Args:
            adom: ADOM name
            
        Returns:
            Device list with installation capabilities
        """
        url = f"/pm/config/adom/{adom}/obj/fmg/device"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def verify_installed_package(
        self,
        device: str,
        package: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Verify package installation on device.
        
        Args:
            device: Device name
            package: Package name
            adom: ADOM name
            
        Returns:
            Verification result
        """
        url = "/securityconsole/install/verify"
        data = {
            "adom": adom,
            "device": device,
            "package": package,
        }
        return await self.client.execute(url, data)

    async def get_install_dependencies(
        self,
        package: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get package installation dependencies.
        
        Args:
            package: Package name
            adom: ADOM name
            
        Returns:
            Dependencies information
        """
        url = f"/pm/config/adom/{adom}/pkg/{package}/dependencies"
        data = await self.client.get(url)
        return data if isinstance(data, dict) else {}

    async def rollback_install(
        self,
        device: str,
        adom: str = "root",
        revision: int | None = None,
    ) -> dict[str, Any]:
        """Rollback to previous installation state.
        
        Args:
            device: Device name
            adom: ADOM name
            revision: Specific revision (optional)
            
        Returns:
            Rollback result
        """
        url = "/securityconsole/install/rollback"
        data = {
            "adom": adom,
            "scope": [{"name": device, "vdom": "root"}],
        }
        if revision:
            data["revision"] = revision
        return await self.client.execute(url, data)

