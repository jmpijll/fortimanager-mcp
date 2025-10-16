"""FortiManager Device Provisioning and Template API operations."""

import logging
from typing import Any

logger = logging.getLogger(__name__)


class ProvisioningAPI:
    """Device provisioning and template management operations.
    
    Handles CLI templates, device profiles, groups, and provisioning operations.
    """

    def __init__(self, client: Any) -> None:
        """Initialize ProvisioningAPI.
        
        Args:
            client: FortiManager API client
        """
        self.client = client

    # =========================================================================
    # CLI Template Methods
    # =========================================================================

    async def list_cli_templates(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List CLI templates in an ADOM.
        
        Args:
            adom: ADOM name
            
        Returns:
            List of CLI templates
        """
        url = f"/pm/config/adom/{adom}/obj/cli/template"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def get_cli_template(
        self,
        name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get CLI template details.
        
        Args:
            name: Template name
            adom: ADOM name
            
        Returns:
            Template details
        """
        url = f"/pm/config/adom/{adom}/obj/cli/template/{name}"
        data = await self.client.get(url)
        return data if isinstance(data, dict) else {}

    async def create_cli_template(
        self,
        name: str,
        script: str,
        adom: str = "root",
        description: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Create a CLI template.
        
        Args:
            name: Template name
            script: Template script content
            adom: ADOM name
            description: Optional description
            **kwargs: Additional template parameters
            
        Returns:
            Created template
        """
        url = f"/pm/config/adom/{adom}/obj/cli/template"
        
        data: dict[str, Any] = {
            "name": name,
            "script": script,
        }
        
        if description:
            data["description"] = description
        
        data.update(kwargs)
        
        result = await self.client.add(url, data)
        return result if isinstance(result, dict) else {}

    async def update_cli_template(
        self,
        name: str,
        adom: str = "root",
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Update a CLI template.
        
        Args:
            name: Template name
            adom: ADOM name
            **kwargs: Fields to update
            
        Returns:
            Updated template
        """
        url = f"/pm/config/adom/{adom}/obj/cli/template/{name}"
        result = await self.client.update(url, kwargs)
        return result if isinstance(result, dict) else {}

    async def delete_cli_template(
        self,
        name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Delete a CLI template.
        
        Args:
            name: Template name
            adom: ADOM name
            
        Returns:
            Deletion status
        """
        url = f"/pm/config/adom/{adom}/obj/cli/template/{name}"
        return await self.client.delete(url)

    # =========================================================================
    # CLI Template Group Methods
    # =========================================================================

    async def list_cli_template_groups(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List CLI template groups in an ADOM.
        
        Args:
            adom: ADOM name
            
        Returns:
            List of template groups
        """
        url = f"/pm/config/adom/{adom}/obj/cli/template-group"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def get_cli_template_group(
        self,
        name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get CLI template group details.
        
        Args:
            name: Template group name
            adom: ADOM name
            
        Returns:
            Template group details
        """
        url = f"/pm/config/adom/{adom}/obj/cli/template-group/{name}"
        data = await self.client.get(url)
        return data if isinstance(data, dict) else {}

    async def create_cli_template_group(
        self,
        name: str,
        adom: str = "root",
        description: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Create a CLI template group.
        
        Args:
            name: Template group name
            adom: ADOM name
            description: Optional description
            **kwargs: Additional group parameters
            
        Returns:
            Created template group
        """
        url = f"/pm/config/adom/{adom}/obj/cli/template-group"
        
        data: dict[str, Any] = {
            "name": name,
        }
        
        if description:
            data["description"] = description
        
        data.update(kwargs)
        
        result = await self.client.add(url, data)
        return result if isinstance(result, dict) else {}

    async def delete_cli_template_group(
        self,
        name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Delete a CLI template group.
        
        Args:
            name: Template group name
            adom: ADOM name
            
        Returns:
            Deletion status
        """
        url = f"/pm/config/adom/{adom}/obj/cli/template-group/{name}"
        return await self.client.delete(url)

    async def add_template_to_group(
        self,
        group_name: str,
        template_name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Add a CLI template to a template group.
        
        Args:
            group_name: Template group name
            template_name: CLI template name to add
            adom: ADOM name
            
        Returns:
            Operation result
        """
        url = f"/pm/config/adom/{adom}/obj/cli/template-group/{group_name}/member"
        
        data = {
            "name": template_name,
        }
        
        result = await self.client.add(url, data)
        return result if isinstance(result, dict) else {}

    async def remove_template_from_group(
        self,
        group_name: str,
        template_name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Remove a CLI template from a template group.
        
        Args:
            group_name: Template group name
            template_name: CLI template name to remove
            adom: ADOM name
            
        Returns:
            Operation result
        """
        url = f"/pm/config/adom/{adom}/obj/cli/template-group/{group_name}/member/{template_name}"
        return await self.client.delete(url)

    async def assign_cli_template(
        self,
        template_name: str,
        devices: list[dict[str, str]],
        adom: str = "root",
    ) -> dict[str, Any]:
        """Assign a CLI template to one or more devices.
        
        Args:
            template_name: CLI template name
            devices: List of device scopes [{"name": "device", "vdom": "vdom"}]
            adom: ADOM name
            
        Returns:
            Operation result
        """
        url = f"/pm/config/adom/{adom}/obj/cli/template/{template_name}/scope member"
        result = await self.client.add(url, devices)
        return result if isinstance(result, dict) else {}

    async def assign_prerun_cli_template(
        self,
        template_name: str,
        devices: list[dict[str, str]],
        adom: str = "root",
    ) -> dict[str, Any]:
        """Assign a pre-run CLI template to one or more devices.
        
        Pre-run templates execute before installation.
        
        Args:
            template_name: CLI template name
            devices: List of device scopes [{"name": "device", "vdom": "vdom"}]
            adom: ADOM name
            
        Returns:
            Operation result
        """
        url = f"/pm/config/adom/{adom}/obj/cli/template/{template_name}/script/scope member"
        result = await self.client.add(url, devices)
        return result if isinstance(result, dict) else {}

    async def assign_cli_template_group(
        self,
        group_name: str,
        devices: list[dict[str, str]],
        adom: str = "root",
    ) -> dict[str, Any]:
        """Assign a CLI template group to one or more devices.
        
        Args:
            group_name: CLI template group name
            devices: List of device scopes [{"name": "device", "vdom": "vdom"}]
            adom: ADOM name
            
        Returns:
            Operation result
        """
        url = f"/pm/config/adom/{adom}/obj/cli/template-group/{group_name}/scope member"
        result = await self.client.add(url, devices)
        return result if isinstance(result, dict) else {}

    async def unassign_cli_template(
        self,
        template_name: str,
        device_name: str,
        vdom: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Unassign a device from a CLI template.
        
        Args:
            template_name: CLI template name
            device_name: Device name
            vdom: VDOM name
            adom: ADOM name
            
        Returns:
            Operation result
        """
        url = f"/pm/config/adom/{adom}/obj/cli/template/{template_name}/scope member"
        
        data = {
            "name": device_name,
            "vdom": vdom,
        }
        
        return await self.client.delete(url, data)

    async def unassign_cli_template_group(
        self,
        group_name: str,
        device_name: str,
        vdom: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Unassign a device from a CLI template group.
        
        Args:
            group_name: CLI template group name
            device_name: Device name
            vdom: VDOM name
            adom: ADOM name
            
        Returns:
            Operation result
        """
        url = f"/pm/config/adom/{adom}/obj/cli/template-group/{group_name}/scope member"
        
        data = {
            "name": device_name,
            "vdom": vdom,
        }
        
        return await self.client.delete(url, data)

    async def validate_cli_template(
        self,
        template_name: str,
        devices: list[dict[str, str]],
        adom: str = "root",
    ) -> dict[str, Any]:
        """Validate/check a CLI template or template group against device(s).
        
        Args:
            template_name: CLI template or template group name
            devices: List of device scopes [{"name": "device", "vdom": "vdom"}]
            adom: ADOM name
            
        Returns:
            Validation result
        """
        url = "/securityconsole/cliprof/check"
        
        data = {
            "adom": adom,
            "cliprof": template_name,
            "scope": devices,
        }
        
        result = await self.client.execute(url, data)
        return result if isinstance(result, dict) else {}

    async def get_cli_template_assigned_devices(
        self,
        template_name: str,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """Get list of devices assigned to a CLI template.
        
        Args:
            template_name: CLI template name
            adom: ADOM name
            
        Returns:
            List of assigned devices
        """
        url = f"/pm/config/adom/{adom}/obj/cli/template/{template_name}/scope member"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def get_cli_template_group_assigned_devices(
        self,
        group_name: str,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """Get list of devices assigned to a CLI template group.
        
        Args:
            group_name: CLI template group name
            adom: ADOM name
            
        Returns:
            List of assigned devices
        """
        url = f"/pm/config/adom/{adom}/obj/cli/template-group/{group_name}/scope member"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    # =========================================================================
    # Device Profile Methods (legacy - kept for backward compatibility)
    # =========================================================================

    async def list_device_profiles(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List device profiles in an ADOM.
        
        Args:
            adom: ADOM name
            
        Returns:
            List of device profiles
        """
        url = f"/pm/devprof/adom/{adom}"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def get_device_profile(
        self,
        name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get device profile details.
        
        Args:
            name: Profile name
            adom: ADOM name
            
        Returns:
            Profile details
        """
        url = f"/pm/devprof/adom/{adom}/{name}"
        data = await self.client.get(url)
        return data if isinstance(data, dict) else {}

    # =========================================================================
    # System Template Methods (device profiles with enhanced operations)
    # =========================================================================

    async def list_system_templates(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List system templates (device profiles) in an ADOM.
        
        System templates are device configuration profiles that can include
        various settings like DNS, NTP, admin, SNMP, interface, routing, etc.
        
        Args:
            adom: ADOM name
            
        Returns:
            List of system templates
        """
        url = f"/pm/devprof/adom/{adom}"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def get_system_template(
        self,
        name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get system template details.
        
        Args:
            name: Template name
            adom: ADOM name
            
        Returns:
            Template details including enabled options and scope members
        """
        url = f"/pm/devprof/adom/{adom}/{name}"
        data = await self.client.get(url)
        return data if isinstance(data, dict) else {}

    async def create_system_template(
        self,
        name: str,
        adom: str = "root",
        description: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Create a new system template.
        
        Args:
            name: Template name
            adom: ADOM name
            description: Optional description
            **kwargs: Additional template parameters
            
        Returns:
            Created template
        """
        url = f"/pm/devprof/adom/{adom}"
        
        data: dict[str, Any] = {
            "name": name,
        }
        
        if description:
            data["description"] = description
        
        data.update(kwargs)
        
        result = await self.client.add(url, data)
        return result if isinstance(result, dict) else {}

    async def update_system_template(
        self,
        name: str,
        adom: str = "root",
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Update a system template.
        
        Args:
            name: Template name
            adom: ADOM name
            **kwargs: Fields to update
            
        Returns:
            Updated template
        """
        url = f"/pm/devprof/adom/{adom}/{name}"
        result = await self.client.update(url, kwargs)
        return result if isinstance(result, dict) else {}

    async def delete_system_template(
        self,
        name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Delete a system template.
        
        Args:
            name: Template name
            adom: ADOM name
            
        Returns:
            Deletion status
        """
        url = f"/pm/devprof/adom/{adom}/{name}"
        return await self.client.delete(url)

    async def clone_system_template(
        self,
        source_name: str,
        new_name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Clone a system template.
        
        Creates a copy of an existing system template with a new name.
        
        Args:
            source_name: Source template name to clone
            new_name: New template name
            adom: ADOM name
            
        Returns:
            Operation result
        """
        url = f"/pm/devprof/adom/{adom}/{source_name}"
        
        data = {
            "name": new_name,
        }
        
        result = await self.client.clone(url, data)
        return result if isinstance(result, dict) else {}

    async def import_system_template(
        self,
        adom: str = "root",
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Import a system template.
        
        Args:
            adom: ADOM name
            **kwargs: Import parameters
            
        Returns:
            Import result
        """
        url = f"/pm/config/adom/{adom}/_devprof/import"
        result = await self.client.execute(url, kwargs)
        return result if isinstance(result, dict) else {}

    async def assign_system_template(
        self,
        template_name: str,
        devices: list[dict[str, str]],
        adom: str = "root",
    ) -> dict[str, Any]:
        """Assign a system template to one or more devices.
        
        Args:
            template_name: System template name
            devices: List of device scopes [{"name": "device", "vdom": "vdom"}]
            adom: ADOM name
            
        Returns:
            Operation result
        """
        url = f"/pm/devprof/adom/{adom}/{template_name}/scope member"
        result = await self.client.add(url, devices)
        return result if isinstance(result, dict) else {}

    async def unassign_system_template(
        self,
        template_name: str,
        device_name: str,
        vdom: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Unassign a device from a system template.
        
        Args:
            template_name: System template name
            device_name: Device name
            vdom: VDOM name
            adom: ADOM name
            
        Returns:
            Operation result
        """
        url = f"/pm/devprof/adom/{adom}/{template_name}/scope member"
        
        data = {
            "name": device_name,
            "vdom": vdom,
        }
        
        return await self.client.delete(url, data)

    async def get_system_template_assigned_devices(
        self,
        template_name: str,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """Get list of devices assigned to a system template.
        
        Args:
            template_name: System template name
            adom: ADOM name
            
        Returns:
            List of assigned devices
        """
        url = f"/pm/devprof/adom/{adom}/{template_name}/scope member"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def get_template_interface_actions(
        self,
        template_name: str,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """Get list of interface actions for a system template.
        
        Args:
            template_name: System template name
            adom: ADOM name
            
        Returns:
            List of interface actions
        """
        url = f"/pm/config/adom/{adom}/devprof/{template_name}/device/template/widget/interface/action-list"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    # =========================================================================
    # Certificate Template Methods
    # =========================================================================

    async def list_certificate_templates(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List certificate templates in an ADOM.
        
        Certificate templates automate certificate enrollment and management
        for managed devices.
        
        Args:
            adom: ADOM name
            
        Returns:
            List of certificate templates
        """
        url = f"/pm/config/adom/{adom}/obj/certificate/template"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def get_certificate_template(
        self,
        name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get certificate template details.
        
        Args:
            name: Template name
            adom: ADOM name
            
        Returns:
            Template details
        """
        url = f"/pm/config/adom/{adom}/obj/certificate/template/{name}"
        data = await self.client.get(url)
        return data if isinstance(data, dict) else {}

    async def create_certificate_template(
        self,
        name: str,
        template_type: str,
        adom: str = "root",
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Create a certificate template.
        
        Can create external (SCEP-based) or local certificate templates.
        
        Args:
            name: Template name
            template_type: Template type - 'external' (SCEP) or 'local'
            adom: ADOM name
            **kwargs: Additional template parameters (organization, country, SCEP server, etc.)
            
        Returns:
            Created template
        """
        url = f"/pm/config/adom/{adom}/obj/certificate/template"
        
        data: dict[str, Any] = {
            "name": name,
            "type": 0 if template_type == "external" else 1,
        }
        
        data.update(kwargs)
        
        result = await self.client.add(url, data)
        return result if isinstance(result, dict) else {}

    async def delete_certificate_template(
        self,
        name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Delete a certificate template.
        
        Args:
            name: Template name
            adom: ADOM name
            
        Returns:
            Deletion status
        """
        url = f"/pm/config/adom/{adom}/obj/certificate/template/{name}"
        return await self.client.delete(url)

    async def enroll_certificate(
        self,
        template_name: str,
        devices: list[dict[str, str]],
        adom: str = "root",
    ) -> dict[str, Any]:
        """Enroll certificates for devices using a certificate template.
        
        This operation triggers certificate enrollment for the specified devices
        using the given certificate template. Returns a task ID that can be
        monitored for completion.
        
        Args:
            template_name: Certificate template name
            devices: List of device scopes [{"name": "device", "vdom": "vdom"}]
            adom: ADOM name
            
        Returns:
            Task information
        """
        url = "/securityconsole/sign/certificate/template"
        
        data = {
            "adom": adom,
            "template": template_name,
            "scope": devices,
        }
        
        result = await self.client.execute(url, data)
        return result if isinstance(result, dict) else {}

    async def assign_certificate_template(
        self,
        template_name: str,
        device_name: str,
        vdom: str,
        local_cert_name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Assign a certificate template to a device.
        
        Creates a per-device mapping in the dynamic local certificate that was
        automatically generated with the certificate template.
        
        Args:
            template_name: Certificate template name (also the dynamic cert name)
            device_name: Device name
            vdom: VDOM name
            local_cert_name: Local certificate name in device DB
            adom: ADOM name
            
        Returns:
            Operation result
        """
        url = f"/pm/config/adom/{adom}/obj/dynamic/certificate/local/{template_name}/dynamic_mapping"
        
        data = {
            "_scope": {
                "name": device_name,
                "vdom": vdom,
            },
            "local-cert": local_cert_name,
        }
        
        result = await self.client.add(url, data)
        return result if isinstance(result, dict) else {}

    async def unassign_certificate_template(
        self,
        template_name: str,
        device_name: str,
        vdom: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Unassign a certificate template from a device.
        
        Removes the per-device mapping from the dynamic local certificate.
        
        Args:
            template_name: Certificate template name
            device_name: Device name
            vdom: VDOM name
            adom: ADOM name
            
        Returns:
            Operation result
        """
        url = f"/pm/config/adom/{adom}/obj/dynamic/certificate/local/{template_name}/dynamic_mapping"
        
        data = {
            "_scope": {
                "name": device_name,
                "vdom": vdom,
            },
        }
        
        return await self.client.delete(url, data)

    # =========================================================================
    # Device Group Methods
    # =========================================================================

    async def list_device_groups(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List device groups in an ADOM.
        
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
        name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get device group details.
        
        Args:
            name: Group name
            adom: ADOM name
            
        Returns:
            Group details including member devices
        """
        url = f"/dvmdb/adom/{adom}/group/{name}"
        data = await self.client.get(url)
        return data if isinstance(data, dict) else {}

    async def create_device_group(
        self,
        name: str,
        adom: str = "root",
        description: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Create a device group.
        
        Args:
            name: Group name
            adom: ADOM name
            description: Optional description
            **kwargs: Additional group parameters
            
        Returns:
            Created group
        """
        url = f"/dvmdb/adom/{adom}/group"
        
        data: dict[str, Any] = {
            "name": name,
        }
        
        if description:
            data["desc"] = description
        
        data.update(kwargs)
        
        result = await self.client.add(url, data)
        return result if isinstance(result, dict) else {}

    async def delete_device_group(
        self,
        name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Delete a device group.
        
        Args:
            name: Group name
            adom: ADOM name
            
        Returns:
            Deletion status
        """
        url = f"/dvmdb/adom/{adom}/group/{name}"
        return await self.client.delete(url)

    async def add_device_to_group(
        self,
        group_name: str,
        device_name: str,
        vdom: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Add a device to a group.
        
        Args:
            group_name: Group name
            device_name: Device name
            vdom: VDOM name
            adom: ADOM name
            
        Returns:
            Operation result
        """
        url = f"/dvmdb/adom/{adom}/group/{group_name}/object member"
        
        data = {
            "name": device_name,
            "vdom": vdom,
        }
        
        result = await self.client.add(url, data)
        return result if isinstance(result, dict) else {}

    # =========================================================================
    # Dynamic Interface Methods
    # =========================================================================

    async def list_dynamic_interfaces(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List dynamic interfaces in an ADOM.
        
        Args:
            adom: ADOM name
            
        Returns:
            List of dynamic interfaces
        """
        url = f"/pm/config/adom/{adom}/obj/dynamic/interface"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def get_dynamic_interface(
        self,
        name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get dynamic interface details.
        
        Args:
            name: Interface name
            adom: ADOM name
            
        Returns:
            Interface details
        """
        url = f"/pm/config/adom/{adom}/obj/dynamic/interface/{name}"
        data = await self.client.get(url)
        return data if isinstance(data, dict) else {}

    async def create_dynamic_interface(
        self,
        name: str,
        adom: str = "root",
        description: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Create a dynamic interface.
        
        Args:
            name: Interface name
            adom: ADOM name
            description: Optional description
            **kwargs: Additional interface parameters
            
        Returns:
            Created interface
        """
        url = f"/pm/config/adom/{adom}/obj/dynamic/interface"
        
        data: dict[str, Any] = {
            "name": name,
        }
        
        if description:
            data["description"] = description
        
        data.update(kwargs)
        
        result = await self.client.add(url, data)
        return result if isinstance(result, dict) else {}

    async def delete_dynamic_interface(
        self,
        name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Delete a dynamic interface.
        
        Args:
            name: Interface name
            adom: ADOM name
            
        Returns:
            Deletion status
        """
        url = f"/pm/config/adom/{adom}/obj/dynamic/interface/{name}"
        return await self.client.delete(url)

    # =========================================================================
    # SD-WAN Template Methods (Phase 4)
    # =========================================================================

    async def list_sdwan_templates(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List SD-WAN templates in an ADOM.
        
        Args:
            adom: ADOM name
            
        Returns:
            List of SD-WAN templates
        """
        url = f"/pm/wanprof/adom/{adom}"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def get_sdwan_template(
        self,
        name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get SD-WAN template details.
        
        Args:
            name: Template name
            adom: ADOM name
            
        Returns:
            Template details
        """
        url = f"/pm/wanprof/adom/{adom}/{name}"
        data = await self.client.get(url)
        return data if isinstance(data, dict) else {}

    async def create_sdwan_template(
        self,
        name: str,
        adom: str = "root",
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Create an SD-WAN template.
        
        Args:
            name: Template name
            adom: ADOM name
            **kwargs: Additional template parameters
            
        Returns:
            Created template
        """
        url = f"/pm/wanprof/adom/{adom}"
        
        data: dict[str, Any] = {
            "name": name,
            "type": "wanprof",
        }
        
        data.update(kwargs)
        
        result = await self.client.add(url, data)
        return result if isinstance(result, dict) else {}

    async def delete_sdwan_template(
        self,
        name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Delete an SD-WAN template.
        
        Args:
            name: Template name
            adom: ADOM name
            
        Returns:
            Deletion status
        """
        url = f"/pm/wanprof/adom/{adom}/{name}"
        return await self.client.delete(url)

    async def assign_sdwan_template(
        self,
        template_name: str,
        devices: list[dict[str, str]],
        adom: str = "root",
    ) -> dict[str, Any]:
        """Assign an SD-WAN template to devices.
        
        Args:
            template_name: SD-WAN template name
            devices: List of device scopes [{"name": "device", "vdom": "vdom"}]
            adom: ADOM name
            
        Returns:
            Operation result
        """
        url = f"/pm/wanprof/adom/{adom}/{template_name}/scope member"
        result = await self.client.add(url, devices)
        return result if isinstance(result, dict) else {}

    async def unassign_sdwan_template(
        self,
        template_name: str,
        device_name: str,
        vdom: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Unassign an SD-WAN template from a device.
        
        Args:
            template_name: SD-WAN template name
            device_name: Device name
            vdom: VDOM name
            adom: ADOM name
            
        Returns:
            Operation result
        """
        url = f"/pm/wanprof/adom/{adom}/{template_name}/scope member"
        
        data = {
            "name": device_name,
            "vdom": vdom,
        }
        
        return await self.client.delete(url, data)

    async def get_sdwan_template_assigned_devices(
        self,
        template_name: str,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """Get devices assigned to an SD-WAN template.
        
        Args:
            template_name: SD-WAN template name
            adom: ADOM name
            
        Returns:
            List of assigned devices
        """
        url = f"/pm/wanprof/adom/{adom}/{template_name}/scope member"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    # =========================================================================
    # IPsec Tunnel Template Methods (Phase 5)
    # =========================================================================

    async def list_ipsec_templates(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List IPsec tunnel templates in an ADOM.
        
        Args:
            adom: ADOM name
            
        Returns:
            List of IPsec templates
        """
        url = f"/pm/config/adom/{adom}/obj/vpn/ipsec/template"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def get_ipsec_template(
        self,
        name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get IPsec tunnel template details.
        
        Args:
            name: Template name
            adom: ADOM name
            
        Returns:
            Template details
        """
        url = f"/pm/config/adom/{adom}/obj/vpn/ipsec/template/{name}"
        data = await self.client.get(url)
        return data if isinstance(data, dict) else {}

    async def create_ipsec_template(
        self,
        name: str,
        adom: str = "root",
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Create an IPsec tunnel template.
        
        Args:
            name: Template name
            adom: ADOM name
            **kwargs: Template parameters
            
        Returns:
            Created template
        """
        url = f"/pm/config/adom/{adom}/obj/vpn/ipsec/template"
        
        data: dict[str, Any] = {
            "name": name,
        }
        
        data.update(kwargs)
        
        result = await self.client.add(url, data)
        return result if isinstance(result, dict) else {}

    async def delete_ipsec_template(
        self,
        name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Delete an IPsec tunnel template.
        
        Args:
            name: Template name
            adom: ADOM name
            
        Returns:
            Deletion status
        """
        url = f"/pm/config/adom/{adom}/obj/vpn/ipsec/template/{name}"
        return await self.client.delete(url)

    async def assign_ipsec_template(
        self,
        template_name: str,
        devices: list[dict[str, str]],
        adom: str = "root",
    ) -> dict[str, Any]:
        """Assign an IPsec template to devices.
        
        Args:
            template_name: IPsec template name
            devices: List of device scopes
            adom: ADOM name
            
        Returns:
            Operation result
        """
        url = f"/pm/config/adom/{adom}/obj/vpn/ipsec/template/{template_name}/scope member"
        result = await self.client.add(url, devices)
        return result if isinstance(result, dict) else {}

    async def unassign_ipsec_template(
        self,
        template_name: str,
        device_name: str,
        vdom: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Unassign an IPsec template from a device.
        
        Args:
            template_name: IPsec template name
            device_name: Device name
            vdom: VDOM name
            adom: ADOM name
            
        Returns:
            Operation result
        """
        url = f"/pm/config/adom/{adom}/obj/vpn/ipsec/template/{template_name}/scope member"
        
        data = {
            "name": device_name,
            "vdom": vdom,
        }
        
        return await self.client.delete(url, data)

    # =========================================================================
    # Static Route Template Methods (Phase 6)
    # =========================================================================

    async def list_static_route_templates(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List static route templates in an ADOM.
        
        Args:
            adom: ADOM name
            
        Returns:
            List of static route templates
        """
        url = f"/pm/config/adom/{adom}/obj/fsp/static-route-template"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def get_static_route_template(
        self,
        name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get static route template details.
        
        Args:
            name: Template name
            adom: ADOM name
            
        Returns:
            Template details
        """
        url = f"/pm/config/adom/{adom}/obj/fsp/static-route-template/{name}"
        data = await self.client.get(url)
        return data if isinstance(data, dict) else {}

    async def create_static_route_template(
        self,
        name: str,
        adom: str = "root",
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Create a static route template.
        
        Args:
            name: Template name
            adom: ADOM name
            **kwargs: Template parameters
            
        Returns:
            Created template
        """
        url = f"/pm/config/adom/{adom}/obj/fsp/static-route-template"
        
        data: dict[str, Any] = {
            "name": name,
        }
        
        data.update(kwargs)
        
        result = await self.client.add(url, data)
        return result if isinstance(result, dict) else {}

    async def delete_static_route_template(
        self,
        name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Delete a static route template.
        
        Args:
            name: Template name
            adom: ADOM name
            
        Returns:
            Deletion status
        """
        url = f"/pm/config/adom/{adom}/obj/fsp/static-route-template/{name}"
        return await self.client.delete(url)

    async def assign_static_route_template(
        self,
        template_name: str,
        devices: list[dict[str, str]],
        adom: str = "root",
    ) -> dict[str, Any]:
        """Assign a static route template to devices.
        
        Args:
            template_name: Static route template name
            devices: List of device scopes
            adom: ADOM name
            
        Returns:
            Operation result
        """
        url = f"/pm/config/adom/{adom}/obj/fsp/static-route-template/{template_name}/scope member"
        result = await self.client.add(url, devices)
        return result if isinstance(result, dict) else {}

    async def unassign_static_route_template(
        self,
        template_name: str,
        device_name: str,
        vdom: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Unassign a static route template from a device.
        
        Args:
            template_name: Static route template name
            device_name: Device name
            vdom: VDOM name
            adom: ADOM name
            
        Returns:
            Operation result
        """
        url = f"/pm/config/adom/{adom}/obj/fsp/static-route-template/{template_name}/scope member"
        
        data = {
            "name": device_name,
            "vdom": vdom,
        }
        
        return await self.client.delete(url, data)

    # =========================================================================
    # Template Group Methods (Phase 7)
    # =========================================================================

    async def create_template_group(
        self,
        name: str,
        description: str = "",
        cli_template_groups: list[str] | None = None,
        fortiap_profiles: list[str] | None = None,
        fortiswitch_templates: list[str] | None = None,
        fortiextender_profiles: list[str] | None = None,
        system_templates: list[str] | None = None,
        ipsec_templates: list[str] | None = None,
        static_route_templates: list[str] | None = None,
        sdwan_templates: list[str] | None = None,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Create a template group bundling multiple templates.
        
        Args:
            name: Template group name
            description: Template group description
            cli_template_groups: List of CLI template group names
            fortiap_profiles: List of FortiAP profile names
            fortiswitch_templates: List of FortiSwitch template names
            fortiextender_profiles: List of FortiExtender profile names
            system_templates: List of system template names (use format "1__templatename")
            ipsec_templates: List of IPsec tunnel template names (use format "4-1__templatename")
            static_route_templates: List of static route template names (use format "4-2__templatename")
            sdwan_templates: List of SD-WAN template names (use format "5__templatename")
            adom: ADOM name
            
        Returns:
            Created template group details
        """
        url = f"/pm/tmplgrp/adom/{adom}"
        
        template_group_setting: dict[str, Any] = {"description": description}
        
        if cli_template_groups:
            template_group_setting["cliprofs"] = cli_template_groups
        if fortiap_profiles:
            template_group_setting["wtpprofs"] = fortiap_profiles
        if fortiswitch_templates:
            template_group_setting["fspprofs"] = fortiswitch_templates
        if fortiextender_profiles:
            template_group_setting["fxtprofs"] = fortiextender_profiles
        
        templates = []
        if system_templates:
            templates.extend(system_templates)
        if ipsec_templates:
            templates.extend(ipsec_templates)
        if static_route_templates:
            templates.extend(static_route_templates)
        if sdwan_templates:
            templates.extend(sdwan_templates)
        
        if templates:
            template_group_setting["templates"] = templates
        
        data = {
            "name": name,
            "type": "tmplgrp",
            "template group setting": template_group_setting,
        }
        
        result = await self.client.add(url, data)
        return result if isinstance(result, dict) else {}

    async def assign_template_group_to_device_group(
        self,
        template_group_name: str,
        device_group_name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Assign a template group to a device group.
        
        Args:
            template_group_name: Template group name
            device_group_name: Device group name
            adom: ADOM name
            
        Returns:
            Operation result
        """
        url = f"/pm/tmplgrp/adom/{adom}"
        
        # First, get the current template group to preserve existing settings
        get_url = f"/pm/tmplgrp/adom/{adom}/{template_group_name}"
        current_data = await self.client.get(get_url)
        
        # Add the device group to scope member
        scope_member = current_data.get("scope member", []) if isinstance(current_data, dict) else []
        scope_member.append({
            "name": device_group_name,
            "is group": 1
        })
        
        update_data = {
            "name": template_group_name,
            "type": "tmplgrp",
            "scope member": scope_member,
            "template group setting": current_data.get("template group setting", {}) if isinstance(current_data, dict) else {}
        }
        
        result = await self.client.update(url, update_data)
        return result if isinstance(result, dict) else {}

    async def delete_template_group(
        self,
        name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Delete a template group.
        
        Args:
            name: Template group name
            adom: ADOM name
            
        Returns:
            Operation result
        """
        url = f"/pm/tmplgrp/adom/{adom}/{name}"
        return await self.client.delete(url)

    # =========================================================================
    # FortiAP Management Methods (Phase 8)
    # =========================================================================

    async def create_model_fortiap(
        self,
        name: str,
        wtp_id: str,
        platform: str,
        device_name: str,
        vdom: str = "root",
        wtp_profile: str | None = None,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Create a model FortiAP device.
        
        Args:
            name: FortiAP name
            wtp_id: Wireless Termination Point ID (serial number)
            platform: FortiAP platform type
            device_name: Managed FortiGate device name
            vdom: VDOM name
            wtp_profile: FortiAP profile name
            adom: ADOM name
            
        Returns:
            Created FortiAP details
        """
        url = f"/pm/config/adom/{adom}/obj/wireless-controller/wtp"
        
        data: dict[str, Any] = {
            "name": name,
            "wtp-id": wtp_id,
            "_platform-type": platform,
            "_is_model": True,
        }
        
        if wtp_profile:
            data["wtp-profile"] = wtp_profile
        
        scope_member = [{"name": device_name, "vdom": vdom}]
        
        result = await self.client.add(url, data, scope_member=scope_member)
        return result if isinstance(result, dict) else {}

    async def list_fortiaps(
        self,
        device_name: str | None = None,
        vdom: str | None = None,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List FortiAP devices in an ADOM.
        
        Args:
            device_name: Specific managed device name (optional)
            vdom: Specific VDOM name (optional)
            adom: ADOM name
            
        Returns:
            List of FortiAP devices
        """
        url = f"/pm/config/adom/{adom}/obj/wireless-controller/wtp"
        
        scope_member = None
        if device_name:
            scope_member = [{"name": device_name, "vdom": vdom or "root"}]
        elif device_name is None and vdom is None:
            # Get all FortiAPs across all devices
            scope_member = [{"name": "All_FortiGate"}]
        
        data = await self.client.get(url, scope_member=scope_member)
        return data if isinstance(data, list) else [data] if data else []

    async def rename_fortiap(
        self,
        current_wtp_id: str,
        new_wtp_id: str,
        device_name: str,
        vdom: str = "root",
        adom: str = "root",
    ) -> dict[str, Any]:
        """Rename a managed FortiAP.
        
        Args:
            current_wtp_id: Current WTP ID
            new_wtp_id: New WTP ID
            device_name: Managed device name
            vdom: VDOM name
            adom: ADOM name
            
        Returns:
            Operation result
        """
        url = f"/pm/config/adom/{adom}/obj/wireless-controller/wtp/{current_wtp_id}"
        
        data = {"wtp-id": new_wtp_id}
        scope_member = [{"name": device_name, "vdom": vdom}]
        
        result = await self.client.update(url, data, scope_member=scope_member)
        return result if isinstance(result, dict) else {}

    async def get_fortiap_status(
        self,
        device_name: str | None = None,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get FortiAP status for managed devices.
        
        Args:
            device_name: Specific managed device name (optional, defaults to all)
            adom: ADOM name
            
        Returns:
            FortiAP status information
        """
        url = "/sys/proxy/json"
        
        target = f"adom/{adom}/device/{device_name}" if device_name else f"adom/{adom}/group/All_FortiGate"
        
        data = {
            "action": "get",
            "resource": "/api/v2/monitor/wifi/managed_ap",
            "target": [target]
        }
        
        result = await self.client.execute(url, data)
        return result if isinstance(result, dict) else {}

    async def refresh_fortiap_status(
        self,
        device_name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Refresh FortiAP status for a managed device.
        
        Args:
            device_name: Managed device name
            adom: ADOM name
            
        Returns:
            Operation result
        """
        url = "/sys/proxy/json"
        
        data = {
            "action": "get",
            "resource": "/api/v2/monitor/wifi/managed_ap?refresh=1",
            "target": [f"adom/{adom}/device/{device_name}"]
        }
        
        result = await self.client.execute(url, data)
        return result if isinstance(result, dict) else {}

    async def update_fortiap_config(
        self,
        wtp_id: str,
        device_name: str,
        config_data: dict[str, Any],
        vdom: str = "root",
        adom: str = "root",
    ) -> dict[str, Any]:
        """Update FortiAP configuration.
        
        Args:
            wtp_id: WTP ID
            device_name: Managed device name
            config_data: Configuration data to update
            vdom: VDOM name
            adom: ADOM name
            
        Returns:
            Operation result
        """
        url = f"/pm/config/adom/{adom}/obj/wireless-controller/wtp/{wtp_id}"
        
        scope_member = [{"name": device_name, "vdom": vdom}]
        
        result = await self.client.update(url, config_data, scope_member=scope_member)
        return result if isinstance(result, dict) else {}

    async def get_fortiap_profile(
        self,
        profile_name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get FortiAP profile details.
        
        Args:
            profile_name: Profile name
            adom: ADOM name
            
        Returns:
            Profile details
        """
        url = f"/pm/config/adom/{adom}/obj/wireless-controller/wtp-profile/{profile_name}"
        data = await self.client.get(url)
        return data if isinstance(data, dict) else {}

    async def delete_fortiap_profile(
        self,
        profile_name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Delete a FortiAP profile.
        
        Args:
            profile_name: Profile name
            adom: ADOM name
            
        Returns:
            Operation result
        """
        url = f"/pm/config/adom/{adom}/obj/wireless-controller/wtp-profile/{profile_name}"
        return await self.client.delete(url)

    async def get_platform_type(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """Get list of supported FortiAP platform types.
        
        Args:
            adom: ADOM name
            
        Returns:
            List of platform types
        """
        url = f"/pm/config/adom/{adom}/obj/wireless-controller/wtp"
        
        # Get with option to retrieve platform types
        data = await self.client.get(url, option="object member")
        return data if isinstance(data, list) else [data] if data else []

    # =========================================================================
    # FortiSwitch Management Methods (Phase 8)
    # =========================================================================

    async def create_model_fortiswitch(
        self,
        switch_id: str,
        platform: str,
        serial_number: str,
        device_name: str,
        template_name: str | None = None,
        vdom: str = "root",
        adom: str = "root",
    ) -> dict[str, Any]:
        """Create a model FortiSwitch device.
        
        Args:
            switch_id: FortiSwitch ID/name
            platform: FortiSwitch platform type
            serial_number: FortiSwitch serial number
            device_name: Managed FortiGate device name
            template_name: FortiSwitch template name (optional)
            vdom: VDOM name
            adom: ADOM name
            
        Returns:
            Created FortiSwitch details
        """
        url = f"/pm/config/adom/{adom}/obj/fsp/managed-switch"
        
        data: dict[str, Any] = {
            "is-model": 1,
            "platform": platform,
            "sn": serial_number,
            "state": 2,
            "switch-id": switch_id,
        }
        
        if template_name:
            data["template"] = template_name
        
        scope_member = [{"name": device_name, "vdom": vdom}]
        
        result = await self.client.add(url, data, scope_member=scope_member)
        return result if isinstance(result, dict) else {}

    async def create_fortiswitch_template(
        self,
        name: str,
        description: str = "",
        adom: str = "root",
    ) -> dict[str, Any]:
        """Create a FortiSwitch template.
        
        Args:
            name: Template name
            description: Template description
            adom: ADOM name
            
        Returns:
            Created template details
        """
        url = f"/pm/config/adom/{adom}/obj/fsp/switch-template"
        
        data = {
            "name": name,
            "description": description,
        }
        
        result = await self.client.add(url, data)
        return result if isinstance(result, dict) else {}

    async def clone_fortiswitch_template(
        self,
        source_name: str,
        new_name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Clone a FortiSwitch template.
        
        Args:
            source_name: Source template name
            new_name: New template name
            adom: ADOM name
            
        Returns:
            Cloned template details
        """
        url = f"/pm/config/adom/{adom}/obj/fsp/switch-template/{source_name}"
        
        data = {"name": new_name}
        
        result = await self.client.clone(url, data)
        return result if isinstance(result, dict) else {}

    async def create_custom_command(
        self,
        command_name: str,
        command: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Create a custom command for FortiSwitch.
        
        Args:
            command_name: Command name
            command: Custom command text
            adom: ADOM name
            
        Returns:
            Created command details
        """
        url = f"/pm/config/adom/{adom}/obj/fsp/custom-command"
        
        data = {
            "command-name": command_name,
            "command": command,
        }
        
        result = await self.client.add(url, data)
        return result if isinstance(result, dict) else {}

    async def add_custom_command_to_template(
        self,
        template_name: str,
        command_name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Add a custom command to a FortiSwitch template.
        
        Args:
            template_name: Template name
            command_name: Custom command name
            adom: ADOM name
            
        Returns:
            Operation result
        """
        url = f"/pm/config/adom/{adom}/obj/fsp/switch-template/{template_name}"
        
        # Get current template to preserve existing settings
        current_data = await self.client.get(url)
        
        custom_commands = current_data.get("custom-command", []) if isinstance(current_data, dict) else []
        if isinstance(custom_commands, str):
            custom_commands = [custom_commands]
        elif not isinstance(custom_commands, list):
            custom_commands = []
        
        custom_commands.append(command_name)
        
        data = {"custom-command": custom_commands}
        
        result = await self.client.update(url, data)
        return result if isinstance(result, dict) else {}

    async def assign_fortiswitch_template(
        self,
        template_name: str,
        switch_id: str,
        device_name: str,
        vdom: str = "root",
        adom: str = "root",
    ) -> dict[str, Any]:
        """Assign a FortiSwitch template to a switch.
        
        Args:
            template_name: Template name
            switch_id: FortiSwitch ID
            device_name: Managed device name
            vdom: VDOM name
            adom: ADOM name
            
        Returns:
            Operation result
        """
        url = f"/pm/config/adom/{adom}/obj/fsp/managed-switch/{switch_id}"
        
        data = {"template": template_name}
        scope_member = [{"name": device_name, "vdom": vdom}]
        
        result = await self.client.update(url, data, scope_member=scope_member)
        return result if isinstance(result, dict) else {}

    async def update_fortiswitch_port(
        self,
        switch_id: str,
        port_name: str,
        port_config: dict[str, Any],
        device_name: str,
        vdom: str = "root",
        adom: str = "root",
    ) -> dict[str, Any]:
        """Update FortiSwitch port configuration.
        
        Args:
            switch_id: FortiSwitch ID
            port_name: Port name
            port_config: Port configuration data
            device_name: Managed device name
            vdom: VDOM name
            adom: ADOM name
            
        Returns:
            Operation result
        """
        url = f"/pm/config/adom/{adom}/obj/fsp/managed-switch/{switch_id}/ports/{port_name}"
        
        scope_member = [{"name": device_name, "vdom": vdom}]
        
        result = await self.client.update(url, port_config, scope_member=scope_member)
        return result if isinstance(result, dict) else {}

    async def import_fortiswitch_template(
        self,
        template_data: dict[str, Any],
        adom: str = "root",
    ) -> dict[str, Any]:
        """Import a FortiSwitch template.
        
        Args:
            template_data: Template data to import
            adom: ADOM name
            
        Returns:
            Import result
        """
        url = f"/pm/config/adom/{adom}/obj/fsp/switch-template"
        
        result = await self.client.add(url, template_data)
        return result if isinstance(result, dict) else {}

    async def get_default_port_config_all(
        self,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get default port configuration for all FortiSwitch models.
        
        Args:
            adom: ADOM name
            
        Returns:
            Default port configurations
        """
        url = f"/pm/config/adom/{adom}/obj/fsp/managed-switch"
        
        # Get with option to retrieve default configurations
        data = await self.client.get(url, option="object member")
        return data if isinstance(data, dict) else {}

    async def get_default_port_config_model(
        self,
        platform: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get default port configuration for a specific FortiSwitch model.
        
        Args:
            platform: FortiSwitch platform type
            adom: ADOM name
            
        Returns:
            Default port configuration for the model
        """
        url = f"/pm/config/adom/{adom}/obj/fsp/managed-switch"
        
        # Get with filter for specific platform
        data = await self.client.get(url, filter=[["platform", "==", platform]])
        return data if isinstance(data, dict) else {}

    async def list_fortiswitches(
        self,
        device_name: str | None = None,
        vdom: str | None = None,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List FortiSwitch devices in an ADOM.
        
        Args:
            device_name: Specific managed device name (optional)
            vdom: Specific VDOM name (optional)
            adom: ADOM name
            
        Returns:
            List of FortiSwitch devices
        """
        url = f"/pm/config/adom/{adom}/obj/fsp/managed-switch"
        
        scope_member = None
        if device_name:
            scope_member = [{"name": device_name, "vdom": vdom or "root"}]
        elif device_name is None and vdom is None:
            # Get all FortiSwitches across all devices
            scope_member = [{"name": "All_FortiGate"}]
        
        data = await self.client.get(url, scope_member=scope_member)
        return data if isinstance(data, list) else [data] if data else []

    async def authorize_fortiswitch(
        self,
        switch_id: str,
        device_name: str,
        vdom: str = "root",
        adom: str = "root",
    ) -> dict[str, Any]:
        """Authorize a FortiSwitch device.
        
        Args:
            switch_id: FortiSwitch ID
            device_name: Managed device name
            vdom: VDOM name
            adom: ADOM name
            
        Returns:
            Operation result
        """
        url = f"/pm/config/adom/{adom}/obj/fsp/managed-switch/{switch_id}"
        
        data = {"authorized": True}
        scope_member = [{"name": device_name, "vdom": vdom}]
        
        result = await self.client.update(url, data, scope_member=scope_member)
        return result if isinstance(result, dict) else {}

    # =========================================================================
    # FortiExtender Management Methods (Phase 8)
    # =========================================================================

    async def create_model_fortiextender(
        self,
        name: str,
        extender_id: str,
        device_name: str,
        profile_name: str | None = None,
        vdom: str = "root",
        adom: str = "root",
    ) -> dict[str, Any]:
        """Create a model FortiExtender device.
        
        Args:
            name: FortiExtender name
            extender_id: FortiExtender ID (serial number)
            device_name: Managed FortiGate device name
            profile_name: FortiExtender profile name (optional)
            vdom: VDOM name
            adom: ADOM name
            
        Returns:
            Created FortiExtender details
        """
        url = f"/pm/config/adom/{adom}/obj/extension-controller/extender"
        
        data: dict[str, Any] = {
            "name": name,
            "ext-name": name,
            "id": extender_id,
            "extension-type": 1,
            "_is_model": True,
            "authorized": True,
        }
        
        if profile_name:
            data["profile"] = profile_name
        
        scope_member = [{"name": device_name, "vdom": vdom}]
        
        result = await self.client.add(url, data, scope_member=scope_member)
        return result if isinstance(result, dict) else {}

    async def list_fortiextenders(
        self,
        device_name: str | None = None,
        vdom: str | None = None,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List FortiExtender devices in an ADOM.
        
        Args:
            device_name: Specific managed device name (optional)
            vdom: Specific VDOM name (optional)
            adom: ADOM name
            
        Returns:
            List of FortiExtender devices
        """
        url = f"/pm/config/adom/{adom}/obj/extension-controller/extender"
        
        scope_member = None
        if device_name:
            scope_member = [{"name": device_name, "vdom": vdom or "root"}]
        elif device_name is None and vdom is None:
            # Get all FortiExtenders across all devices
            scope_member = [{"name": "All_FortiGate"}]
        
        data = await self.client.get(url, scope_member=scope_member)
        return data if isinstance(data, list) else [data] if data else []

    async def delete_fortiextender(
        self,
        name: str,
        device_name: str,
        vdom: str = "root",
        adom: str = "root",
    ) -> dict[str, Any]:
        """Delete a FortiExtender device.
        
        Args:
            name: FortiExtender name
            device_name: Managed device name
            vdom: VDOM name
            adom: ADOM name
            
        Returns:
            Operation result
        """
        url = f"/pm/config/adom/{adom}/obj/extension-controller/extender/{name}"
        
        scope_member = [{"name": device_name, "vdom": vdom}]
        
        return await self.client.delete(url, scope_member=scope_member)

    async def get_fortiextender_status(
        self,
        device_name: str | None = None,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get FortiExtender status for managed devices.
        
        Args:
            device_name: Specific managed device name (optional, defaults to all)
            adom: ADOM name
            
        Returns:
            FortiExtender status information
        """
        url = "/sys/proxy/json"
        
        target = f"adom/{adom}/device/{device_name}" if device_name else f"adom/{adom}/group/All_FortiGate"
        
        data = {
            "action": "get",
            "resource": "/api/v2/monitor/extension-controller/extender",
            "target": [target]
        }
        
        result = await self.client.execute(url, data)
        return result if isinstance(result, dict) else {}

    # =========================================================================
    # Advanced Template Operations Methods (Phase 9)
    # =========================================================================

    async def validate_provisioning_template(
        self,
        template_type: str,
        template_name: str,
        device_name: str,
        vdom: str = "root",
        adom: str = "root",
    ) -> dict[str, Any]:
        """Validate a provisioning template before deployment.
        
        Args:
            template_type: Template type (cli, system, sdwan, ipsec, static-route)
            template_name: Template name
            device_name: Target device name
            vdom: VDOM name
            adom: ADOM name
            
        Returns:
            Validation result
        """
        url = "/pm/config/_template/validate"
        
        data = {
            "template-type": template_type,
            "template-name": template_name,
            "scope member": [{"name": device_name, "vdom": vdom}],
            "adom": adom,
        }
        
        result = await self.client.execute(url, data)
        return result if isinstance(result, dict) else {}

    async def get_firmware_upgrade_preview(
        self,
        device_name: str,
        firmware_version: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get firmware upgrade preview for a device.
        
        Args:
            device_name: Device name
            firmware_version: Target firmware version
            adom: ADOM name
            
        Returns:
            Firmware upgrade preview
        """
        url = "/um/image/upgrade/preview"
        
        data = {
            "adom": adom,
            "device": device_name,
            "version": firmware_version,
        }
        
        result = await self.client.execute(url, data)
        return result if isinstance(result, dict) else {}

    async def get_firmware_upgrade_report(
        self,
        device_name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get firmware upgrade report for a device.
        
        Args:
            device_name: Device name
            adom: ADOM name
            
        Returns:
            Firmware upgrade report
        """
        url = "/um/image/upgrade/report"
        
        data = {
            "adom": adom,
            "device": device_name,
        }
        
        result = await self.client.execute(url, data)
        return result if isinstance(result, dict) else {}

    async def export_templates(
        self,
        template_names: list[str],
        template_type: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Export provisioning templates.
        
        Args:
            template_names: List of template names to export
            template_type: Template type (cli, system, sdwan, ipsec, static-route, fortiswitch)
            adom: ADOM name
            
        Returns:
            Export data
        """
        url = "/pm/config/_template/export"
        
        data = {
            "template-type": template_type,
            "templates": template_names,
            "adom": adom,
        }
        
        result = await self.client.execute(url, data)
        return result if isinstance(result, dict) else {}

