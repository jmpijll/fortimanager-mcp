"""MCP tools for device provisioning and template management."""

import logging
from typing import Any

from fortimanager_mcp.api.provisioning import ProvisioningAPI
from fortimanager_mcp.server import get_fmg_client, mcp

logger = logging.getLogger(__name__)


def _get_provisioning_api() -> ProvisioningAPI:
    """Get Provisioning API instance with FortiManager client."""
    client = get_fmg_client()
    if client is None:
        raise RuntimeError("FortiManager client not initialized")
    return ProvisioningAPI(client)


# =============================================================================
# CLI Template Tools
# =============================================================================


@mcp.tool()
async def list_cli_templates(adom: str = "root") -> dict[str, Any]:
    """List all CLI templates in an ADOM.
    
    CLI templates are reusable configuration scripts that can be applied
    to multiple devices. They support:
    - FortiOS CLI commands
    - Variable substitution
    - Conditional logic
    - Device-specific customization
    
    Common use cases:
    - Interface provisioning
    - VLAN configuration
    - Hardware switch port configuration
    - Standard security settings
    
    Args:
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with status and list of templates
    """
    api = _get_provisioning_api()
    templates = await api.list_cli_templates(adom=adom)
    return {
        "status": "success",
        "count": len(templates),
        "templates": templates,
    }


@mcp.tool()
async def get_cli_template(
    name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Get detailed information about a specific CLI template.
    
    Args:
        name: Template name
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with status and template details including script content
    """
    api = _get_provisioning_api()
    template = await api.get_cli_template(name=name, adom=adom)
    return {
        "status": "success",
        "template": template,
    }


@mcp.tool()
async def create_cli_template(
    name: str,
    script: str,
    adom: str = "root",
    description: str | None = None,
) -> dict[str, Any]:
    """Create a new CLI template.
    
    CLI templates can contain FortiOS CLI commands with optional variables
    for dynamic configuration.
    
    Example script content:
    ```
    config system interface
        edit "port1"
            set vdom "root"
            set ip 192.168.1.1 255.255.255.0
            set allowaccess ping https ssh
        next
    end
    ```
    
    Args:
        name: Template name
        script: Template script content (FortiOS CLI commands)
        adom: ADOM name (default: root)
        description: Optional description
    
    Returns:
        Dictionary with status and created template details
    """
    api = _get_provisioning_api()
    result = await api.create_cli_template(
        name=name,
        script=script,
        adom=adom,
        description=description,
    )
    return {
        "status": "success",
        "template": result,
    }


@mcp.tool()
async def delete_cli_template(
    name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Delete a CLI template.
    
    WARNING: Ensure the template is not in use by any template groups
    or device configurations before deletion.
    
    Args:
        name: Template name
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with deletion status
    """
    api = _get_provisioning_api()
    result = await api.delete_cli_template(name=name, adom=adom)
    return {
        "status": "success",
        "result": result,
    }


@mcp.tool()
async def update_cli_template(
    name: str,
    adom: str = "root",
    script: str | None = None,
    description: str | None = None,
) -> dict[str, Any]:
    """Update an existing CLI template.
    
    Update the script content or other properties of a CLI template.
    
    Args:
        name: Template name
        adom: ADOM name (default: root)
        script: Updated template script content
        description: Updated description
    
    Returns:
        Dictionary with status and updated template details
    """
    api = _get_provisioning_api()
    
    kwargs: dict[str, Any] = {}
    if script is not None:
        kwargs["script"] = script
    if description is not None:
        kwargs["description"] = description
    
    result = await api.update_cli_template(name=name, adom=adom, **kwargs)
    return {
        "status": "success",
        "template": result,
    }


@mcp.tool()
async def assign_cli_template(
    template_name: str,
    device_name: str,
    vdom: str = "root",
    adom: str = "root",
) -> dict[str, Any]:
    """Assign a CLI template to a device.
    
    Assigns a CLI template to one or more devices, making it available
    for installation. The template will be applied during the next
    device configuration install/preview operation.
    
    Args:
        template_name: CLI template name
        device_name: Device name to assign to
        vdom: VDOM name (default: root)
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with assignment status
    """
    api = _get_provisioning_api()
    devices = [{"name": device_name, "vdom": vdom}]
    result = await api.assign_cli_template(
        template_name=template_name,
        devices=devices,
        adom=adom,
    )
    return {
        "status": "success",
        "result": result,
    }


@mcp.tool()
async def assign_prerun_cli_template(
    template_name: str,
    device_name: str,
    vdom: str = "root",
    adom: str = "root",
) -> dict[str, Any]:
    """Assign a pre-run CLI template to a device.
    
    Pre-run CLI templates execute before the main configuration installation.
    They are useful for:
    - Preparing the device environment
    - Setting up prerequisites
    - Running validation checks
    
    Args:
        template_name: CLI template name
        device_name: Device name to assign to
        vdom: VDOM name (default: root)
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with assignment status
    """
    api = _get_provisioning_api()
    devices = [{"name": device_name, "vdom": vdom}]
    result = await api.assign_prerun_cli_template(
        template_name=template_name,
        devices=devices,
        adom=adom,
    )
    return {
        "status": "success",
        "result": result,
    }


@mcp.tool()
async def unassign_cli_template(
    template_name: str,
    device_name: str,
    vdom: str = "root",
    adom: str = "root",
) -> dict[str, Any]:
    """Unassign a device from a CLI template.
    
    Removes the assignment of a CLI template from a device.
    The template will no longer be applied to this device.
    
    Args:
        template_name: CLI template name
        device_name: Device name to unassign
        vdom: VDOM name (default: root)
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with unassignment status
    """
    api = _get_provisioning_api()
    result = await api.unassign_cli_template(
        template_name=template_name,
        device_name=device_name,
        vdom=vdom,
        adom=adom,
    )
    return {
        "status": "success",
        "result": result,
    }


@mcp.tool()
async def get_cli_template_assigned_devices(
    template_name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Get list of devices assigned to a CLI template.
    
    Returns all devices that have this CLI template assigned,
    showing which devices will receive the template configuration.
    
    Args:
        template_name: CLI template name
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with status and list of assigned devices
    """
    api = _get_provisioning_api()
    devices = await api.get_cli_template_assigned_devices(
        template_name=template_name,
        adom=adom,
    )
    return {
        "status": "success",
        "count": len(devices),
        "devices": devices,
    }


@mcp.tool()
async def validate_cli_template(
    template_name: str,
    device_name: str,
    vdom: str = "root",
    adom: str = "root",
) -> dict[str, Any]:
    """Validate a CLI template against a device.
    
    Checks if a CLI template is valid for a specific device without
    actually applying it. This helps identify syntax errors or
    configuration conflicts before installation.
    
    Args:
        template_name: CLI template or template group name
        device_name: Device name to validate against
        vdom: VDOM name (default: root)
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with validation result
    """
    api = _get_provisioning_api()
    devices = [{"name": device_name, "vdom": vdom}]
    result = await api.validate_cli_template(
        template_name=template_name,
        devices=devices,
        adom=adom,
    )
    return {
        "status": "success",
        "validation": result,
    }


# =============================================================================
# CLI Template Group Tools
# =============================================================================


@mcp.tool()
async def list_cli_template_groups(adom: str = "root") -> dict[str, Any]:
    """List all CLI template groups in an ADOM.
    
    Template groups organize multiple CLI templates into logical sets
    that can be applied together to devices. This allows for:
    - Organized template management
    - Batch template application
    - Role-based configuration sets
    
    Args:
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with status and list of template groups
    """
    api = _get_provisioning_api()
    groups = await api.list_cli_template_groups(adom=adom)
    return {
        "status": "success",
        "count": len(groups),
        "groups": groups,
    }


@mcp.tool()
async def get_cli_template_group(
    name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Get detailed information about a specific CLI template group.
    
    Args:
        name: Template group name
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with status and group details including member templates
    """
    api = _get_provisioning_api()
    group = await api.get_cli_template_group(name=name, adom=adom)
    return {
        "status": "success",
        "group": group,
    }


@mcp.tool()
async def create_cli_template_group(
    name: str,
    adom: str = "root",
    description: str | None = None,
) -> dict[str, Any]:
    """Create a new CLI template group.
    
    Template groups organize multiple CLI templates that should be
    applied together to devices.
    
    Args:
        name: Template group name
        adom: ADOM name (default: root)
        description: Optional description
    
    Returns:
        Dictionary with status and created group details
    """
    api = _get_provisioning_api()
    result = await api.create_cli_template_group(
        name=name,
        adom=adom,
        description=description,
    )
    return {
        "status": "success",
        "group": result,
    }


@mcp.tool()
async def delete_cli_template_group(
    name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Delete a CLI template group.
    
    WARNING: Ensure the template group is not assigned to any devices
    before deletion.
    
    Args:
        name: Template group name
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with deletion status
    """
    api = _get_provisioning_api()
    result = await api.delete_cli_template_group(name=name, adom=adom)
    return {
        "status": "success",
        "result": result,
    }


@mcp.tool()
async def add_template_to_group(
    group_name: str,
    template_name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Add a CLI template to a template group.
    
    Adds an existing CLI template as a member of a template group.
    All templates in a group will be applied together when the group
    is assigned to a device.
    
    Args:
        group_name: Template group name
        template_name: CLI template name to add
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with operation status
    """
    api = _get_provisioning_api()
    result = await api.add_template_to_group(
        group_name=group_name,
        template_name=template_name,
        adom=adom,
    )
    return {
        "status": "success",
        "result": result,
    }


@mcp.tool()
async def remove_template_from_group(
    group_name: str,
    template_name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Remove a CLI template from a template group.
    
    Removes a template from the group's member list.
    
    Args:
        group_name: Template group name
        template_name: CLI template name to remove
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with operation status
    """
    api = _get_provisioning_api()
    result = await api.remove_template_from_group(
        group_name=group_name,
        template_name=template_name,
        adom=adom,
    )
    return {
        "status": "success",
        "result": result,
    }


@mcp.tool()
async def assign_cli_template_group(
    group_name: str,
    device_name: str,
    vdom: str = "root",
    adom: str = "root",
) -> dict[str, Any]:
    """Assign a CLI template group to a device.
    
    Assigns all templates in a template group to a device.
    This allows applying multiple related templates in one operation.
    
    Args:
        group_name: CLI template group name
        device_name: Device name to assign to
        vdom: VDOM name (default: root)
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with assignment status
    """
    api = _get_provisioning_api()
    devices = [{"name": device_name, "vdom": vdom}]
    result = await api.assign_cli_template_group(
        group_name=group_name,
        devices=devices,
        adom=adom,
    )
    return {
        "status": "success",
        "result": result,
    }


@mcp.tool()
async def unassign_cli_template_group(
    group_name: str,
    device_name: str,
    vdom: str = "root",
    adom: str = "root",
) -> dict[str, Any]:
    """Unassign a device from a CLI template group.
    
    Removes the assignment of a CLI template group from a device.
    The templates in the group will no longer be applied to this device.
    
    Args:
        group_name: CLI template group name
        device_name: Device name to unassign
        vdom: VDOM name (default: root)
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with unassignment status
    """
    api = _get_provisioning_api()
    result = await api.unassign_cli_template_group(
        group_name=group_name,
        device_name=device_name,
        vdom=vdom,
        adom=adom,
    )
    return {
        "status": "success",
        "result": result,
    }


@mcp.tool()
async def get_cli_template_group_assigned_devices(
    group_name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Get list of devices assigned to a CLI template group.
    
    Returns all devices that have this CLI template group assigned,
    showing which devices will receive all the group's templates.
    
    Args:
        group_name: CLI template group name
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with status and list of assigned devices
    """
    api = _get_provisioning_api()
    devices = await api.get_cli_template_group_assigned_devices(
        group_name=group_name,
        adom=adom,
    )
    return {
        "status": "success",
        "count": len(devices),
        "devices": devices,
    }


# =============================================================================
# System Template Tools
# =============================================================================


@mcp.tool()
async def list_system_templates(adom: str = "root") -> dict[str, Any]:
    """List all system templates (device profiles) in an ADOM.
    
    System templates are comprehensive device configuration profiles that can
    include multiple system-wide settings:
    - DNS configuration
    - NTP servers
    - Email settings
    - Admin users and settings
    - SNMP configuration
    - Replacement messages
    - FortiGuard settings
    - Log settings
    - Interface configuration
    - Routing configuration
    
    Args:
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with status and list of system templates
    """
    api = _get_provisioning_api()
    templates = await api.list_system_templates(adom=adom)
    return {
        "status": "success",
        "count": len(templates),
        "templates": templates,
    }


@mcp.tool()
async def get_system_template(
    name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Get detailed information about a specific system template.
    
    Returns complete template configuration including enabled options,
    scope members (assigned devices), and all template settings.
    
    Args:
        name: Template name
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with status and template details
    """
    api = _get_provisioning_api()
    template = await api.get_system_template(name=name, adom=adom)
    return {
        "status": "success",
        "template": template,
    }


@mcp.tool()
async def create_system_template(
    name: str,
    adom: str = "root",
    description: str | None = None,
) -> dict[str, Any]:
    """Create a new system template.
    
    System templates provide centralized configuration management for
    multiple devices, ensuring consistent system-wide settings across
    your FortiGate infrastructure.
    
    Args:
        name: Template name
        adom: ADOM name (default: root)
        description: Optional description
    
    Returns:
        Dictionary with status and created template details
    """
    api = _get_provisioning_api()
    result = await api.create_system_template(
        name=name,
        adom=adom,
        description=description,
    )
    return {
        "status": "success",
        "template": result,
    }


@mcp.tool()
async def update_system_template(
    name: str,
    adom: str = "root",
    description: str | None = None,
) -> dict[str, Any]:
    """Update an existing system template.
    
    Args:
        name: Template name
        adom: ADOM name (default: root)
        description: Updated description
    
    Returns:
        Dictionary with status and updated template details
    """
    api = _get_provisioning_api()
    
    kwargs: dict[str, Any] = {}
    if description is not None:
        kwargs["description"] = description
    
    result = await api.update_system_template(name=name, adom=adom, **kwargs)
    return {
        "status": "success",
        "template": result,
    }


@mcp.tool()
async def delete_system_template(
    name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Delete a system template.
    
    WARNING: Ensure the template is not assigned to any devices before deletion.
    
    Args:
        name: Template name
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with deletion status
    """
    api = _get_provisioning_api()
    result = await api.delete_system_template(name=name, adom=adom)
    return {
        "status": "success",
        "result": result,
    }


@mcp.tool()
async def clone_system_template(
    source_name: str,
    new_name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Clone an existing system template.
    
    Creates a complete copy of a system template with a new name,
    preserving all configuration settings from the source template.
    This is useful for:
    - Creating template variations
    - Using an existing template as a starting point
    - Backup before making changes
    
    Args:
        source_name: Source template name to clone
        new_name: New template name
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with cloning status
    """
    api = _get_provisioning_api()
    result = await api.clone_system_template(
        source_name=source_name,
        new_name=new_name,
        adom=adom,
    )
    return {
        "status": "success",
        "result": result,
    }


@mcp.tool()
async def assign_system_template(
    template_name: str,
    device_name: str,
    vdom: str = "root",
    adom: str = "root",
) -> dict[str, Any]:
    """Assign a system template to a device.
    
    Applies the system template's configuration to the specified device.
    The template settings will be applied during the next device installation.
    
    Args:
        template_name: System template name
        device_name: Device name to assign to
        vdom: VDOM name (default: root)
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with assignment status
    """
    api = _get_provisioning_api()
    devices = [{"name": device_name, "vdom": vdom}]
    result = await api.assign_system_template(
        template_name=template_name,
        devices=devices,
        adom=adom,
    )
    return {
        "status": "success",
        "result": result,
    }


@mcp.tool()
async def unassign_system_template(
    template_name: str,
    device_name: str,
    vdom: str = "root",
    adom: str = "root",
) -> dict[str, Any]:
    """Unassign a device from a system template.
    
    Removes the system template assignment from the specified device.
    The template settings will no longer be applied to this device.
    
    Args:
        template_name: System template name
        device_name: Device name to unassign
        vdom: VDOM name (default: root)
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with unassignment status
    """
    api = _get_provisioning_api()
    result = await api.unassign_system_template(
        template_name=template_name,
        device_name=device_name,
        vdom=vdom,
        adom=adom,
    )
    return {
        "status": "success",
        "result": result,
    }


@mcp.tool()
async def get_system_template_assigned_devices(
    template_name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Get list of devices assigned to a system template.
    
    Returns all devices that have this system template assigned,
    showing which devices will receive the template configuration.
    
    Args:
        template_name: System template name
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with status and list of assigned devices
    """
    api = _get_provisioning_api()
    devices = await api.get_system_template_assigned_devices(
        template_name=template_name,
        adom=adom,
    )
    return {
        "status": "success",
        "count": len(devices),
        "devices": devices,
    }


@mcp.tool()
async def get_template_interface_actions(
    template_name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Get list of interface actions for a system template.
    
    Returns the interface widget actions configured in the system template.
    Interface actions define how interfaces should be configured on
    managed devices.
    
    Args:
        template_name: System template name
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with status and list of interface actions
    """
    api = _get_provisioning_api()
    actions = await api.get_template_interface_actions(
        template_name=template_name,
        adom=adom,
    )
    return {
        "status": "success",
        "count": len(actions),
        "actions": actions,
    }


# =============================================================================
# Certificate Template Tools
# =============================================================================


@mcp.tool()
async def list_certificate_templates(adom: str = "root") -> dict[str, Any]:
    """List all certificate templates in an ADOM.
    
    Certificate templates automate the process of enrolling and managing
    certificates for managed devices. They support:
    - External SCEP-based enrollment
    - Local certificate management
    - Automatic certificate renewal
    - Per-device certificate mapping
    
    Args:
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with status and list of certificate templates
    """
    api = _get_provisioning_api()
    templates = await api.list_certificate_templates(adom=adom)
    return {
        "status": "success",
        "count": len(templates),
        "templates": templates,
    }


@mcp.tool()
async def get_certificate_template(
    name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Get detailed information about a specific certificate template.
    
    Returns complete template configuration including enrollment settings,
    SCEP parameters, and organizational details.
    
    Args:
        name: Template name
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with status and template details
    """
    api = _get_provisioning_api()
    template = await api.get_certificate_template(name=name, adom=adom)
    return {
        "status": "success",
        "template": template,
    }


@mcp.tool()
async def create_certificate_template(
    name: str,
    template_type: str,
    adom: str = "root",
    organization: str | None = None,
    country: str | None = None,
) -> dict[str, Any]:
    """Create a new certificate template.
    
    Certificate templates can be:
    - External (SCEP-based): Automatically enrolls certificates from a SCEP server
    - Local: Uses locally-managed certificates
    
    Args:
        name: Template name
        template_type: Template type - 'external' for SCEP or 'local' for local certs
        adom: ADOM name (default: root)
        organization: Organization name (for external templates)
        country: Country code (for external templates)
    
    Returns:
        Dictionary with status and created template details
    """
    api = _get_provisioning_api()
    
    kwargs: dict[str, Any] = {}
    if organization:
        kwargs["organization"] = organization
    if country:
        kwargs["country"] = country
    
    result = await api.create_certificate_template(
        name=name,
        template_type=template_type,
        adom=adom,
        **kwargs,
    )
    return {
        "status": "success",
        "template": result,
    }


@mcp.tool()
async def delete_certificate_template(
    name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Delete a certificate template.
    
    WARNING: Deleting a certificate template also deletes the automatically
    generated dynamic local certificate with the same name.
    
    Args:
        name: Template name
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with deletion status
    """
    api = _get_provisioning_api()
    result = await api.delete_certificate_template(name=name, adom=adom)
    return {
        "status": "success",
        "result": result,
    }


@mcp.tool()
async def enroll_certificate(
    template_name: str,
    device_name: str,
    vdom: str = "root",
    adom: str = "root",
) -> dict[str, Any]:
    """Enroll a certificate for a device using a certificate template.
    
    This operation triggers certificate enrollment for the specified device.
    The enrollment process:
    1. Generates a certificate request on the device
    2. Submits it to the SCEP server (for external templates)
    3. Stores the certificate in the device DB
    4. Creates a per-device mapping in the dynamic local certificate
    
    Returns a task ID that can be monitored for completion.
    
    Args:
        template_name: Certificate template name
        device_name: Device name
        vdom: VDOM name (default: root)
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with task ID and status
    """
    api = _get_provisioning_api()
    devices = [{"name": device_name, "vdom": vdom}]
    result = await api.enroll_certificate(
        template_name=template_name,
        devices=devices,
        adom=adom,
    )
    return {
        "status": "success",
        "task": result,
    }


@mcp.tool()
async def assign_certificate_template(
    template_name: str,
    device_name: str,
    local_cert_name: str,
    vdom: str = "root",
    adom: str = "root",
) -> dict[str, Any]:
    """Assign a certificate template to a device.
    
    Creates a per-device mapping in the dynamic local certificate that was
    automatically generated with the certificate template. This allows
    referencing device-specific certificates in ADOM database objects.
    
    Use this when a device already has a certificate (e.g., uploaded manually)
    and you want to associate it with the certificate template for ADOM
    object referencing.
    
    Args:
        template_name: Certificate template name
        device_name: Device name
        local_cert_name: Name of the existing certificate in device DB
        vdom: VDOM name (default: root)
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with assignment status
    """
    api = _get_provisioning_api()
    result = await api.assign_certificate_template(
        template_name=template_name,
        device_name=device_name,
        vdom=vdom,
        local_cert_name=local_cert_name,
        adom=adom,
    )
    return {
        "status": "success",
        "result": result,
    }


@mcp.tool()
async def unassign_certificate_template(
    template_name: str,
    device_name: str,
    vdom: str = "root",
    adom: str = "root",
) -> dict[str, Any]:
    """Unassign a certificate template from a device.
    
    Removes the per-device mapping from the dynamic local certificate.
    The certificate remains in the device DB but is no longer mapped to
    the certificate template.
    
    Args:
        template_name: Certificate template name
        device_name: Device name
        vdom: VDOM name (default: root)
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with unassignment status
    """
    api = _get_provisioning_api()
    result = await api.unassign_certificate_template(
        template_name=template_name,
        device_name=device_name,
        vdom=vdom,
        adom=adom,
    )
    return {
        "status": "success",
        "result": result,
    }


# =============================================================================
# SD-WAN Template Tools (Phase 4)
# =============================================================================


@mcp.tool()
async def list_sdwan_templates(adom: str = "root") -> dict[str, Any]:
    """List all SD-WAN templates in an ADOM.
    
    SD-WAN templates provide centralized configuration for SD-WAN deployments
    including zones, members, health checks, and traffic steering rules.
    
    Args:
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with status and list of SD-WAN templates
    """
    api = _get_provisioning_api()
    templates = await api.list_sdwan_templates(adom=adom)
    return {
        "status": "success",
        "count": len(templates),
        "templates": templates,
    }


@mcp.tool()
async def get_sdwan_template(
    name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Get detailed information about a specific SD-WAN template.
    
    Args:
        name: Template name
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with status and template details
    """
    api = _get_provisioning_api()
    template = await api.get_sdwan_template(name=name, adom=adom)
    return {
        "status": "success",
        "template": template,
    }


@mcp.tool()
async def create_sdwan_template(
    name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Create a new SD-WAN template.
    
    Args:
        name: Template name
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with status and created template details
    """
    api = _get_provisioning_api()
    result = await api.create_sdwan_template(name=name, adom=adom)
    return {
        "status": "success",
        "template": result,
    }


@mcp.tool()
async def delete_sdwan_template(
    name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Delete an SD-WAN template.
    
    Args:
        name: Template name
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with deletion status
    """
    api = _get_provisioning_api()
    result = await api.delete_sdwan_template(name=name, adom=adom)
    return {
        "status": "success",
        "result": result,
    }


@mcp.tool()
async def assign_sdwan_template(
    template_name: str,
    device_name: str,
    vdom: str = "root",
    adom: str = "root",
) -> dict[str, Any]:
    """Assign an SD-WAN template to a device.
    
    Args:
        template_name: SD-WAN template name
        device_name: Device name to assign to
        vdom: VDOM name (default: root)
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with assignment status
    """
    api = _get_provisioning_api()
    devices = [{"name": device_name, "vdom": vdom}]
    result = await api.assign_sdwan_template(
        template_name=template_name,
        devices=devices,
        adom=adom,
    )
    return {
        "status": "success",
        "result": result,
    }


@mcp.tool()
async def unassign_sdwan_template(
    template_name: str,
    device_name: str,
    vdom: str = "root",
    adom: str = "root",
) -> dict[str, Any]:
    """Unassign an SD-WAN template from a device.
    
    Args:
        template_name: SD-WAN template name
        device_name: Device name to unassign
        vdom: VDOM name (default: root)
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with unassignment status
    """
    api = _get_provisioning_api()
    result = await api.unassign_sdwan_template(
        template_name=template_name,
        device_name=device_name,
        vdom=vdom,
        adom=adom,
    )
    return {
        "status": "success",
        "result": result,
    }


@mcp.tool()
async def get_sdwan_template_assigned_devices(
    template_name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Get list of devices assigned to an SD-WAN template.
    
    Args:
        template_name: SD-WAN template name
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with status and list of assigned devices
    """
    api = _get_provisioning_api()
    devices = await api.get_sdwan_template_assigned_devices(
        template_name=template_name,
        adom=adom,
    )
    return {
        "status": "success",
        "count": len(devices),
        "devices": devices,
    }


# =============================================================================
# IPsec Tunnel Template Tools (Phase 5)
# =============================================================================


@mcp.tool()
async def list_ipsec_templates(adom: str = "root") -> dict[str, Any]:
    """List all IPsec tunnel templates in an ADOM.
    
    IPsec tunnel templates provide centralized VPN tunnel configuration
    that can be applied to multiple devices.
    
    Args:
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with status and list of IPsec templates
    """
    api = _get_provisioning_api()
    templates = await api.list_ipsec_templates(adom=adom)
    return {
        "status": "success",
        "count": len(templates),
        "templates": templates,
    }


@mcp.tool()
async def get_ipsec_template(
    name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Get detailed information about a specific IPsec tunnel template.
    
    Args:
        name: Template name
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with status and template details
    """
    api = _get_provisioning_api()
    template = await api.get_ipsec_template(name=name, adom=adom)
    return {
        "status": "success",
        "template": template,
    }


@mcp.tool()
async def create_ipsec_template(
    name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Create a new IPsec tunnel template.
    
    Args:
        name: Template name
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with status and created template details
    """
    api = _get_provisioning_api()
    result = await api.create_ipsec_template(name=name, adom=adom)
    return {
        "status": "success",
        "template": result,
    }


@mcp.tool()
async def delete_ipsec_template(
    name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Delete an IPsec tunnel template.
    
    Args:
        name: Template name
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with deletion status
    """
    api = _get_provisioning_api()
    result = await api.delete_ipsec_template(name=name, adom=adom)
    return {
        "status": "success",
        "result": result,
    }


@mcp.tool()
async def assign_ipsec_template(
    template_name: str,
    device_name: str,
    vdom: str = "root",
    adom: str = "root",
) -> dict[str, Any]:
    """Assign an IPsec tunnel template to a device.
    
    Args:
        template_name: IPsec template name
        device_name: Device name to assign to
        vdom: VDOM name (default: root)
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with assignment status
    """
    api = _get_provisioning_api()
    devices = [{"name": device_name, "vdom": vdom}]
    result = await api.assign_ipsec_template(
        template_name=template_name,
        devices=devices,
        adom=adom,
    )
    return {
        "status": "success",
        "result": result,
    }


@mcp.tool()
async def unassign_ipsec_template(
    template_name: str,
    device_name: str,
    vdom: str = "root",
    adom: str = "root",
) -> dict[str, Any]:
    """Unassign an IPsec tunnel template from a device.
    
    Args:
        template_name: IPsec template name
        device_name: Device name to unassign
        vdom: VDOM name (default: root)
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with unassignment status
    """
    api = _get_provisioning_api()
    result = await api.unassign_ipsec_template(
        template_name=template_name,
        device_name=device_name,
        vdom=vdom,
        adom=adom,
    )
    return {
        "status": "success",
        "result": result,
    }


# =============================================================================
# Static Route Template Tools (Phase 6)
# =============================================================================


@mcp.tool()
async def list_static_route_templates(adom: str = "root") -> dict[str, Any]:
    """List all static route templates in an ADOM.
    
    Static route templates provide centralized routing configuration
    that can be applied to multiple devices.
    
    Args:
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with status and list of static route templates
    """
    api = _get_provisioning_api()
    templates = await api.list_static_route_templates(adom=adom)
    return {
        "status": "success",
        "count": len(templates),
        "templates": templates,
    }


@mcp.tool()
async def get_static_route_template(
    name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Get detailed information about a specific static route template.
    
    Args:
        name: Template name
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with status and template details
    """
    api = _get_provisioning_api()
    template = await api.get_static_route_template(name=name, adom=adom)
    return {
        "status": "success",
        "template": template,
    }


@mcp.tool()
async def create_static_route_template(
    name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Create a new static route template.
    
    Args:
        name: Template name
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with status and created template details
    """
    api = _get_provisioning_api()
    result = await api.create_static_route_template(name=name, adom=adom)
    return {
        "status": "success",
        "template": result,
    }


@mcp.tool()
async def delete_static_route_template(
    name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Delete a static route template.
    
    Args:
        name: Template name
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with deletion status
    """
    api = _get_provisioning_api()
    result = await api.delete_static_route_template(name=name, adom=adom)
    return {
        "status": "success",
        "result": result,
    }


@mcp.tool()
async def assign_static_route_template(
    template_name: str,
    device_name: str,
    vdom: str = "root",
    adom: str = "root",
) -> dict[str, Any]:
    """Assign a static route template to a device.
    
    Args:
        template_name: Static route template name
        device_name: Device name to assign to
        vdom: VDOM name (default: root)
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with assignment status
    """
    api = _get_provisioning_api()
    devices = [{"name": device_name, "vdom": vdom}]
    result = await api.assign_static_route_template(
        template_name=template_name,
        devices=devices,
        adom=adom,
    )
    return {
        "status": "success",
        "result": result,
    }


@mcp.tool()
async def unassign_static_route_template(
    template_name: str,
    device_name: str,
    vdom: str = "root",
    adom: str = "root",
) -> dict[str, Any]:
    """Unassign a static route template from a device.
    
    Args:
        template_name: Static route template name
        device_name: Device name to unassign
        vdom: VDOM name (default: root)
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with unassignment status
    """
    api = _get_provisioning_api()
    result = await api.unassign_static_route_template(
        template_name=template_name,
        device_name=device_name,
        vdom=vdom,
        adom=adom,
    )
    return {
        "status": "success",
        "result": result,
    }


# =============================================================================
# Device Profile Tools (legacy - kept for backward compatibility)
# =============================================================================


@mcp.tool()
async def list_device_profiles(adom: str = "root") -> dict[str, Any]:
    """List all device profiles in an ADOM.
    
    Device profiles (also called provisioning templates) define standardized
    configurations for devices. They include:
    - System settings
    - Interface configurations
    - Routing settings
    - Security profiles
    - Policy packages
    
    Profiles enable consistent device provisioning and reduce configuration
    errors by applying tested, standardized configurations.
    
    Args:
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with status and list of profiles
    """
    api = _get_provisioning_api()
    profiles = await api.list_device_profiles(adom=adom)
    return {
        "status": "success",
        "count": len(profiles),
        "profiles": profiles,
    }


@mcp.tool()
async def get_device_profile(
    name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Get detailed information about a specific device profile.
    
    Args:
        name: Profile name
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with status and profile details
    """
    api = _get_provisioning_api()
    profile = await api.get_device_profile(name=name, adom=adom)
    return {
        "status": "success",
        "profile": profile,
    }


# =============================================================================
# Device Group Tools
# =============================================================================


@mcp.tool()
async def list_device_groups(adom: str = "root") -> dict[str, Any]:
    """List all device groups in an ADOM.
    
    Device groups organize managed devices for:
    - Bulk operations (policy installation, firmware upgrades)
    - Policy assignment
    - Monitoring and reporting
    - Access control
    
    Groups can be based on:
    - Location (branches, datacenters)
    - Function (firewalls, VPN gateways)
    - Environment (production, staging)
    
    Args:
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with status and list of groups
    """
    api = _get_provisioning_api()
    groups = await api.list_device_groups(adom=adom)
    return {
        "status": "success",
        "count": len(groups),
        "groups": groups,
    }


@mcp.tool()
async def get_device_group(
    name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Get detailed information about a specific device group.
    
    Includes group metadata and list of member devices.
    
    Args:
        name: Group name
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with status and group details including members
    """
    api = _get_provisioning_api()
    group = await api.get_device_group(name=name, adom=adom)
    return {
        "status": "success",
        "group": group,
    }


@mcp.tool()
async def create_device_group(
    name: str,
    adom: str = "root",
    description: str | None = None,
) -> dict[str, Any]:
    """Create a new device group.
    
    After creating a group, use add_device_to_group to add member devices.
    
    Args:
        name: Group name
        adom: ADOM name (default: root)
        description: Optional description
    
    Returns:
        Dictionary with status and created group details
    """
    api = _get_provisioning_api()
    result = await api.create_device_group(
        name=name,
        adom=adom,
        description=description,
    )
    return {
        "status": "success",
        "group": result,
    }


@mcp.tool()
async def delete_device_group(
    name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Delete a device group.
    
    This operation does not delete the member devices, only the group itself.
    
    Args:
        name: Group name
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with deletion status
    """
    api = _get_provisioning_api()
    result = await api.delete_device_group(name=name, adom=adom)
    return {
        "status": "success",
        "result": result,
    }


@mcp.tool()
async def add_device_to_group(
    group_name: str,
    device_name: str,
    vdom: str = "root",
    adom: str = "root",
) -> dict[str, Any]:
    """Add a device to a device group.
    
    Args:
        group_name: Group name
        device_name: Device name to add
        vdom: VDOM name on the device (default: root)
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with operation status
    """
    api = _get_provisioning_api()
    result = await api.add_device_to_group(
        group_name=group_name,
        device_name=device_name,
        vdom=vdom,
        adom=adom,
    )
    return {
        "status": "success",
        "result": result,
    }


# =============================================================================
# Dynamic Interface Tools
# =============================================================================


@mcp.tool()
async def list_dynamic_interfaces(adom: str = "root") -> dict[str, Any]:
    """List all dynamic interfaces in an ADOM.
    
    Dynamic interfaces are interface objects that can be mapped to
    physical interfaces on managed devices. They enable:
    - Centralized interface management
    - Consistent interface naming across devices
    - Interface role assignment
    - Policy application based on interface mappings
    
    Common use cases:
    - WAN interface definitions
    - LAN zone interfaces
    - DMZ interfaces
    - Management interfaces
    
    Args:
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with status and list of interfaces
    """
    api = _get_provisioning_api()
    interfaces = await api.list_dynamic_interfaces(adom=adom)
    return {
        "status": "success",
        "count": len(interfaces),
        "interfaces": interfaces,
    }


@mcp.tool()
async def get_dynamic_interface(
    name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Get detailed information about a specific dynamic interface.
    
    Args:
        name: Interface name
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with status and interface details
    """
    api = _get_provisioning_api()
    interface = await api.get_dynamic_interface(name=name, adom=adom)
    return {
        "status": "success",
        "interface": interface,
    }


@mcp.tool()
async def create_dynamic_interface(
    name: str,
    adom: str = "root",
    description: str | None = None,
) -> dict[str, Any]:
    """Create a new dynamic interface.
    
    Dynamic interfaces must be mapped to physical interfaces on
    specific devices after creation.
    
    Args:
        name: Interface name
        adom: ADOM name (default: root)
        description: Optional description
    
    Returns:
        Dictionary with status and created interface details
    """
    api = _get_provisioning_api()
    result = await api.create_dynamic_interface(
        name=name,
        adom=adom,
        description=description,
    )
    return {
        "status": "success",
        "interface": result,
    }


@mcp.tool()
async def delete_dynamic_interface(
    name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Delete a dynamic interface.
    
    WARNING: Ensure the interface is not referenced in any policies
    or device configurations before deletion.
    
    Args:
        name: Interface name
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with deletion status
    """
    api = _get_provisioning_api()
    result = await api.delete_dynamic_interface(name=name, adom=adom)
    return {
        "status": "success",
        "result": result,
    }


# =============================================================================
# Template Group Tools (Phase 7)
# =============================================================================

@mcp.tool()
async def create_template_group(
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
    
    Template groups allow bundling multiple template types for coordinated
    deployment to devices or device groups. Supports CLI templates, FortiAP/
    FortiSwitch/FortiExtender profiles, and various provisioning templates.
    
    Args:
        name: Template group name
        description: Template group description
        cli_template_groups: List of CLI template group names
        fortiap_profiles: List of FortiAP profile names
        fortiswitch_templates: List of FortiSwitch template names
        fortiextender_profiles: List of FortiExtender profile names
        system_templates: List of system template names (format: "1__templatename")
        ipsec_templates: List of IPsec tunnel template names (format: "4-1__templatename")
        static_route_templates: List of static route template names (format: "4-2__templatename")
        sdwan_templates: List of SD-WAN template names (format: "5__templatename")
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with created template group details
    """
    api = _get_provisioning_api()
    result = await api.create_template_group(
        name=name,
        description=description,
        cli_template_groups=cli_template_groups,
        fortiap_profiles=fortiap_profiles,
        fortiswitch_templates=fortiswitch_templates,
        fortiextender_profiles=fortiextender_profiles,
        system_templates=system_templates,
        ipsec_templates=ipsec_templates,
        static_route_templates=static_route_templates,
        sdwan_templates=sdwan_templates,
        adom=adom,
    )
    return {"status": "success", "template_group": result}


@mcp.tool()
async def assign_template_group_to_device_group(
    template_group_name: str,
    device_group_name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Assign a template group to a device group.
    
    Associates a template group with a device group for coordinated template
    deployment across all devices in the group.
    
    Args:
        template_group_name: Template group name
        device_group_name: Device group name
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with assignment status
    """
    api = _get_provisioning_api()
    result = await api.assign_template_group_to_device_group(
        template_group_name=template_group_name,
        device_group_name=device_group_name,
        adom=adom,
    )
    return {"status": "success", "result": result}


@mcp.tool()
async def delete_template_group(
    name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Delete a template group.
    
    WARNING: Ensure the template group is not assigned to any device groups
    before deletion.
    
    Args:
        name: Template group name
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with deletion status
    """
    api = _get_provisioning_api()
    result = await api.delete_template_group(name=name, adom=adom)
    return {"status": "success", "result": result}


# =============================================================================
# FortiAP Management Tools (Phase 8)
# =============================================================================

@mcp.tool()
async def create_model_fortiap(
    name: str,
    wtp_id: str,
    platform: str,
    device_name: str,
    vdom: str = "root",
    wtp_profile: str | None = None,
    adom: str = "root",
) -> dict[str, Any]:
    """Create a model FortiAP device for centralized wireless management.
    
    Model FortiAPs are declared in FortiManager for centralized configuration
    management before being deployed to managed FortiGate devices.
    
    Args:
        name: FortiAP name
        wtp_id: Wireless Termination Point ID (serial number)
        platform: FortiAP platform type (e.g., "FortiAP-231F")
        device_name: Managed FortiGate device name
        vdom: VDOM name (default: root)
        wtp_profile: FortiAP profile name (optional)
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with created FortiAP details
    """
    api = _get_provisioning_api()
    result = await api.create_model_fortiap(
        name=name,
        wtp_id=wtp_id,
        platform=platform,
        device_name=device_name,
        vdom=vdom,
        wtp_profile=wtp_profile,
        adom=adom,
    )
    return {"status": "success", "fortiap": result}


@mcp.tool()
async def list_fortiaps(
    device_name: str | None = None,
    vdom: str | None = None,
    adom: str = "root",
) -> dict[str, Any]:
    """List FortiAP devices in an ADOM.
    
    Retrieve all FortiAP devices managed by FortiManager, optionally filtered
    by specific managed device.
    
    Args:
        device_name: Specific managed device name (optional, defaults to all)
        vdom: Specific VDOM name (optional)
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with list of FortiAP devices
    """
    api = _get_provisioning_api()
    result = await api.list_fortiaps(
        device_name=device_name,
        vdom=vdom,
        adom=adom,
    )
    return {"count": len(result), "fortiaps": result}


@mcp.tool()
async def rename_fortiap(
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
        vdom: VDOM name (default: root)
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with rename status
    """
    api = _get_provisioning_api()
    result = await api.rename_fortiap(
        current_wtp_id=current_wtp_id,
        new_wtp_id=new_wtp_id,
        device_name=device_name,
        vdom=vdom,
        adom=adom,
    )
    return {"status": "success", "result": result}


@mcp.tool()
async def get_fortiap_status(
    device_name: str | None = None,
    adom: str = "root",
) -> dict[str, Any]:
    """Get FortiAP status for managed devices.
    
    Retrieves real-time status information for FortiAP devices managed by
    FortiGate devices in the specified ADOM.
    
    Args:
        device_name: Specific managed device name (optional, defaults to all)
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with FortiAP status information
    """
    api = _get_provisioning_api()
    result = await api.get_fortiap_status(device_name=device_name, adom=adom)
    return {"status": "success", "fortiap_status": result}


@mcp.tool()
async def refresh_fortiap_status(
    device_name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Refresh FortiAP status for a managed device.
    
    Forces an immediate refresh of FortiAP status information from the
    specified managed FortiGate device.
    
    Args:
        device_name: Managed device name
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with refreshed FortiAP status
    """
    api = _get_provisioning_api()
    result = await api.refresh_fortiap_status(device_name=device_name, adom=adom)
    return {"status": "success", "result": result}


@mcp.tool()
async def update_fortiap_config(
    wtp_id: str,
    device_name: str,
    config_data: dict[str, Any],
    vdom: str = "root",
    adom: str = "root",
) -> dict[str, Any]:
    """Update FortiAP configuration.
    
    Updates configuration settings for a specific FortiAP device.
    
    Args:
        wtp_id: WTP ID
        device_name: Managed device name
        config_data: Configuration data to update
        vdom: VDOM name (default: root)
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with update status
    """
    api = _get_provisioning_api()
    result = await api.update_fortiap_config(
        wtp_id=wtp_id,
        device_name=device_name,
        config_data=config_data,
        vdom=vdom,
        adom=adom,
    )
    return {"status": "success", "result": result}


@mcp.tool()
async def get_fortiap_profile(
    profile_name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Get FortiAP profile details.
    
    Retrieves configuration details for a specific FortiAP profile.
    
    Args:
        profile_name: Profile name
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with profile details
    """
    api = _get_provisioning_api()
    result = await api.get_fortiap_profile(profile_name=profile_name, adom=adom)
    return {"profile": result}


@mcp.tool()
async def delete_fortiap_profile(
    profile_name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Delete a FortiAP profile.
    
    WARNING: Ensure the profile is not assigned to any FortiAPs before deletion.
    
    Args:
        profile_name: Profile name
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with deletion status
    """
    api = _get_provisioning_api()
    result = await api.delete_fortiap_profile(profile_name=profile_name, adom=adom)
    return {"status": "success", "result": result}


@mcp.tool()
async def get_platform_type(
    adom: str = "root",
) -> dict[str, Any]:
    """Get list of supported FortiAP platform types.
    
    Retrieves all supported FortiAP hardware platforms for the ADOM.
    
    Args:
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with list of platform types
    """
    api = _get_provisioning_api()
    result = await api.get_platform_type(adom=adom)
    return {"platforms": result}


# =============================================================================
# FortiSwitch Management Tools (Phase 8)
# =============================================================================

@mcp.tool()
async def create_model_fortiswitch(
    switch_id: str,
    platform: str,
    serial_number: str,
    device_name: str,
    template_name: str | None = None,
    vdom: str = "root",
    adom: str = "root",
) -> dict[str, Any]:
    """Create a model FortiSwitch device for centralized switch management.
    
    Model FortiSwitches are declared in FortiManager for centralized configuration
    management before being deployed to managed FortiGate devices.
    
    Args:
        switch_id: FortiSwitch ID/name
        platform: FortiSwitch platform type (e.g., "FortiSwitch-108F-FPOE")
        serial_number: FortiSwitch serial number
        device_name: Managed FortiGate device name
        template_name: FortiSwitch template name (optional)
        vdom: VDOM name (default: root)
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with created FortiSwitch details
    """
    api = _get_provisioning_api()
    result = await api.create_model_fortiswitch(
        switch_id=switch_id,
        platform=platform,
        serial_number=serial_number,
        device_name=device_name,
        template_name=template_name,
        vdom=vdom,
        adom=adom,
    )
    return {"status": "success", "fortiswitch": result}


@mcp.tool()
async def create_fortiswitch_template(
    name: str,
    description: str = "",
    adom: str = "root",
) -> dict[str, Any]:
    """Create a FortiSwitch template.
    
    Templates define standardized port configurations and settings for
    FortiSwitch devices.
    
    Args:
        name: Template name
        description: Template description
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with created template details
    """
    api = _get_provisioning_api()
    result = await api.create_fortiswitch_template(
        name=name,
        description=description,
        adom=adom,
    )
    return {"status": "success", "template": result}


@mcp.tool()
async def clone_fortiswitch_template(
    source_name: str,
    new_name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Clone a FortiSwitch template.
    
    Creates a copy of an existing FortiSwitch template with a new name.
    
    Args:
        source_name: Source template name
        new_name: New template name
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with cloned template details
    """
    api = _get_provisioning_api()
    result = await api.clone_fortiswitch_template(
        source_name=source_name,
        new_name=new_name,
        adom=adom,
    )
    return {"status": "success", "template": result}


@mcp.tool()
async def create_custom_command(
    command_name: str,
    command: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Create a custom command for FortiSwitch.
    
    Custom commands allow execution of specific FortiSwitch CLI commands
    during template deployment.
    
    Args:
        command_name: Command name
        command: Custom command text
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with created command details
    """
    api = _get_provisioning_api()
    result = await api.create_custom_command(
        command_name=command_name,
        command=command,
        adom=adom,
    )
    return {"status": "success", "command": result}


@mcp.tool()
async def add_custom_command_to_template(
    template_name: str,
    command_name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Add a custom command to a FortiSwitch template.
    
    Associates a previously created custom command with a FortiSwitch template.
    
    Args:
        template_name: Template name
        command_name: Custom command name
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with operation status
    """
    api = _get_provisioning_api()
    result = await api.add_custom_command_to_template(
        template_name=template_name,
        command_name=command_name,
        adom=adom,
    )
    return {"status": "success", "result": result}


@mcp.tool()
async def assign_fortiswitch_template(
    template_name: str,
    switch_id: str,
    device_name: str,
    vdom: str = "root",
    adom: str = "root",
) -> dict[str, Any]:
    """Assign a FortiSwitch template to a switch.
    
    Applies a FortiSwitch template configuration to a specific switch device.
    
    Args:
        template_name: Template name
        switch_id: FortiSwitch ID
        device_name: Managed device name
        vdom: VDOM name (default: root)
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with assignment status
    """
    api = _get_provisioning_api()
    result = await api.assign_fortiswitch_template(
        template_name=template_name,
        switch_id=switch_id,
        device_name=device_name,
        vdom=vdom,
        adom=adom,
    )
    return {"status": "success", "result": result}


@mcp.tool()
async def update_fortiswitch_port(
    switch_id: str,
    port_name: str,
    port_config: dict[str, Any],
    device_name: str,
    vdom: str = "root",
    adom: str = "root",
) -> dict[str, Any]:
    """Update FortiSwitch port configuration.
    
    Modifies configuration settings for a specific port on a FortiSwitch device.
    
    Args:
        switch_id: FortiSwitch ID
        port_name: Port name (e.g., "port1")
        port_config: Port configuration data
        device_name: Managed device name
        vdom: VDOM name (default: root)
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with update status
    """
    api = _get_provisioning_api()
    result = await api.update_fortiswitch_port(
        switch_id=switch_id,
        port_name=port_name,
        port_config=port_config,
        device_name=device_name,
        vdom=vdom,
        adom=adom,
    )
    return {"status": "success", "result": result}


@mcp.tool()
async def import_fortiswitch_template(
    template_data: dict[str, Any],
    adom: str = "root",
) -> dict[str, Any]:
    """Import a FortiSwitch template.
    
    Imports a FortiSwitch template from external data.
    
    Args:
        template_data: Template data to import
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with import status
    """
    api = _get_provisioning_api()
    result = await api.import_fortiswitch_template(
        template_data=template_data,
        adom=adom,
    )
    return {"status": "success", "result": result}


@mcp.tool()
async def get_default_port_config_all(
    adom: str = "root",
) -> dict[str, Any]:
    """Get default port configuration for all FortiSwitch models.
    
    Retrieves the default port configurations for all supported FortiSwitch
    hardware models.
    
    Args:
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with default port configurations
    """
    api = _get_provisioning_api()
    result = await api.get_default_port_config_all(adom=adom)
    return {"configurations": result}


@mcp.tool()
async def get_default_port_config_model(
    platform: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Get default port configuration for a specific FortiSwitch model.
    
    Retrieves the default port configuration for a specific FortiSwitch
    hardware platform.
    
    Args:
        platform: FortiSwitch platform type
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with default port configuration
    """
    api = _get_provisioning_api()
    result = await api.get_default_port_config_model(platform=platform, adom=adom)
    return {"configuration": result}


@mcp.tool()
async def list_fortiswitches(
    device_name: str | None = None,
    vdom: str | None = None,
    adom: str = "root",
) -> dict[str, Any]:
    """List FortiSwitch devices in an ADOM.
    
    Retrieves all FortiSwitch devices managed by FortiManager, optionally
    filtered by specific managed device.
    
    Args:
        device_name: Specific managed device name (optional, defaults to all)
        vdom: Specific VDOM name (optional)
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with list of FortiSwitch devices
    """
    api = _get_provisioning_api()
    result = await api.list_fortiswitches(
        device_name=device_name,
        vdom=vdom,
        adom=adom,
    )
    return {"count": len(result), "fortiswitches": result}


@mcp.tool()
async def authorize_fortiswitch(
    switch_id: str,
    device_name: str,
    vdom: str = "root",
    adom: str = "root",
) -> dict[str, Any]:
    """Authorize a FortiSwitch device.
    
    Authorizes a FortiSwitch device for management by the specified FortiGate.
    
    Args:
        switch_id: FortiSwitch ID
        device_name: Managed device name
        vdom: VDOM name (default: root)
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with authorization status
    """
    api = _get_provisioning_api()
    result = await api.authorize_fortiswitch(
        switch_id=switch_id,
        device_name=device_name,
        vdom=vdom,
        adom=adom,
    )
    return {"status": "success", "result": result}


# =============================================================================
# FortiExtender Management Tools (Phase 8)
# =============================================================================

@mcp.tool()
async def create_model_fortiextender(
    name: str,
    extender_id: str,
    device_name: str,
    profile_name: str | None = None,
    vdom: str = "root",
    adom: str = "root",
) -> dict[str, Any]:
    """Create a model FortiExtender device for cellular connectivity management.
    
    Model FortiExtenders are declared in FortiManager for centralized configuration
    management before being deployed to managed FortiGate devices.
    
    Args:
        name: FortiExtender name
        extender_id: FortiExtender ID (serial number)
        device_name: Managed FortiGate device name
        profile_name: FortiExtender profile name (optional)
        vdom: VDOM name (default: root)
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with created FortiExtender details
    """
    api = _get_provisioning_api()
    result = await api.create_model_fortiextender(
        name=name,
        extender_id=extender_id,
        device_name=device_name,
        profile_name=profile_name,
        vdom=vdom,
        adom=adom,
    )
    return {"status": "success", "fortiextender": result}


@mcp.tool()
async def list_fortiextenders(
    device_name: str | None = None,
    vdom: str | None = None,
    adom: str = "root",
) -> dict[str, Any]:
    """List FortiExtender devices in an ADOM.
    
    Retrieves all FortiExtender devices managed by FortiManager, optionally
    filtered by specific managed device.
    
    Args:
        device_name: Specific managed device name (optional, defaults to all)
        vdom: Specific VDOM name (optional)
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with list of FortiExtender devices
    """
    api = _get_provisioning_api()
    result = await api.list_fortiextenders(
        device_name=device_name,
        vdom=vdom,
        adom=adom,
    )
    return {"count": len(result), "fortiextenders": result}


@mcp.tool()
async def delete_fortiextender(
    name: str,
    device_name: str,
    vdom: str = "root",
    adom: str = "root",
) -> dict[str, Any]:
    """Delete a FortiExtender device.
    
    WARNING: Ensure the FortiExtender is not actively in use before deletion.
    
    Args:
        name: FortiExtender name
        device_name: Managed device name
        vdom: VDOM name (default: root)
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with deletion status
    """
    api = _get_provisioning_api()
    result = await api.delete_fortiextender(
        name=name,
        device_name=device_name,
        vdom=vdom,
        adom=adom,
    )
    return {"status": "success", "result": result}


@mcp.tool()
async def get_fortiextender_status(
    device_name: str | None = None,
    adom: str = "root",
) -> dict[str, Any]:
    """Get FortiExtender status for managed devices.
    
    Retrieves real-time status information for FortiExtender devices managed
    by FortiGate devices in the specified ADOM.
    
    Args:
        device_name: Specific managed device name (optional, defaults to all)
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with FortiExtender status information
    """
    api = _get_provisioning_api()
    result = await api.get_fortiextender_status(device_name=device_name, adom=adom)
    return {"status": "success", "fortiextender_status": result}


# =============================================================================
# Advanced Template Operations Tools (Phase 9)
# =============================================================================

@mcp.tool()
async def validate_provisioning_template(
    template_type: str,
    template_name: str,
    device_name: str,
    vdom: str = "root",
    adom: str = "root",
) -> dict[str, Any]:
    """Validate a provisioning template before deployment.
    
    Validates template syntax and compatibility with target device before
    actual deployment.
    
    Args:
        template_type: Template type (cli, system, sdwan, ipsec, static-route)
        template_name: Template name
        device_name: Target device name
        vdom: VDOM name (default: root)
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with validation results
    """
    api = _get_provisioning_api()
    result = await api.validate_provisioning_template(
        template_type=template_type,
        template_name=template_name,
        device_name=device_name,
        vdom=vdom,
        adom=adom,
    )
    return {"validation": result}


@mcp.tool()
async def get_firmware_upgrade_preview(
    device_name: str,
    firmware_version: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Get firmware upgrade preview for a device.
    
    Previews the impact of upgrading a device to a specific firmware version,
    including compatibility checks and potential issues.
    
    Args:
        device_name: Device name
        firmware_version: Target firmware version
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with firmware upgrade preview
    """
    api = _get_provisioning_api()
    result = await api.get_firmware_upgrade_preview(
        device_name=device_name,
        firmware_version=firmware_version,
        adom=adom,
    )
    return {"preview": result}


@mcp.tool()
async def get_firmware_upgrade_report(
    device_name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Get firmware upgrade report for a device.
    
    Retrieves detailed report of firmware upgrade history and status for
    a specific device.
    
    Args:
        device_name: Device name
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with firmware upgrade report
    """
    api = _get_provisioning_api()
    result = await api.get_firmware_upgrade_report(
        device_name=device_name,
        adom=adom,
    )
    return {"report": result}


@mcp.tool()
async def export_templates(
    template_names: list[str],
    template_type: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Export provisioning templates.
    
    Exports specified provisioning templates for backup or migration to
    another FortiManager instance.
    
    Args:
        template_names: List of template names to export
        template_type: Template type (cli, system, sdwan, ipsec, static-route, fortiswitch)
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with exported template data
    """
    api = _get_provisioning_api()
    result = await api.export_templates(
        template_names=template_names,
        template_type=template_type,
        adom=adom,
    )
    return {"export_data": result}

