"""MCP tools for device management operations."""

import logging
from typing import Any

from fortimanager_mcp.api.adoms import ADOMAPI
from fortimanager_mcp.api.devices import DeviceAPI
from fortimanager_mcp.server import get_fmg_client, mcp

logger = logging.getLogger(__name__)


def _get_device_api() -> DeviceAPI:
    """Get DeviceAPI instance."""
    client = get_fmg_client()
    if not client:
        raise RuntimeError("FortiManager client not initialized")
    return DeviceAPI(client)


@mcp.tool()
async def list_devices(adom: str | None = None) -> dict[str, Any]:
    """List all managed FortiGate devices.

    Lists all devices managed by FortiManager, optionally filtered by ADOM.
    Returns device information including name, IP, OS version, connection status, etc.

    Args:
        adom: Optional ADOM name to filter devices (None for all ADOMs)

    Returns:
        Dictionary with list of devices and their details

    Example:
        # List all devices
        result = list_devices()

        # List devices in specific ADOM
        result = list_devices(adom="root")
    """
    try:
        api = _get_device_api()
        devices = await api.list_devices(adom=adom)

        return {
            "status": "success",
            "count": len(devices),
            "devices": [
                {
                    "name": d.name,
                    "ip": d.ip,
                    "os_version": d.os_ver,
                    "platform": d.platform_str,
                    "serial_number": d.sn,
                    "connected": d.is_connected,
                    "connection_status": d.conn_status,
                }
                for d in devices
            ],
        }
    except Exception as e:
        logger.error(f"Error listing devices: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_device_details(name: str, adom: str | None = None) -> dict[str, Any]:
    """Get detailed information about a specific device.

    Retrieves comprehensive information about a managed FortiGate device including
    OS version, platform, VDOMs, connection status, and more.

    Args:
        name: Device name
        adom: Optional ADOM name

    Returns:
        Dictionary with detailed device information

    Example:
        result = get_device_details(name="FGT-Branch-01", adom="root")
    """
    try:
        api = _get_device_api()
        device = await api.get_device(name=name, adom=adom)

        return {
            "status": "success",
            "device": {
                "name": device.name,
                "ip": device.ip,
                "os_type": device.os_type,
                "os_version": device.os_ver,
                "maintenance_release": device.mr,
                "build": device.build,
                "platform": device.platform_str,
                "serial_number": device.sn,
                "connection_status": device.conn_status,
                "connected": device.is_connected,
                "ha_mode": device.ha_mode,
                "vdoms": device.vdom,
            },
        }
    except Exception as e:
        logger.error(f"Error getting device details for {name}: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def install_device_settings(
    device: str,
    adom: str = "root",
    vdom: str = "root",
    comments: str | None = None,
) -> dict[str, Any]:
    """Install pending device settings to a FortiGate device.

    Pushes pending network and system configuration changes to the device.
    This does NOT install security settings (objects, policies).
    Returns a task ID for monitoring the installation progress.

    Args:
        device: Device name
        adom: ADOM name (default: "root")
        vdom: VDOM name (default: "root")
        comments: Optional installation comments

    Returns:
        Dictionary with installation task information

    Example:
        result = install_device_settings(
            device="FGT-Branch-01",
            adom="root",
            comments="Installing interface changes"
        )
    """
    try:
        api = _get_device_api()
        result = await api.install_device_settings(
            device=device,
            adom=adom,
            vdom=vdom,
            comments=comments,
        )

        task_id = result.get("task")
        return {
            "status": "success",
            "message": f"Device settings installation initiated for {device}",
            "task_id": task_id,
            "note": "Use get_task_status tool to monitor installation progress",
        }
    except Exception as e:
        logger.error(f"Error installing device settings for {device}: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def list_adoms() -> dict[str, Any]:
    """List all Administrative Domains (ADOMs).

    Retrieves a list of all ADOMs configured in FortiManager.
    ADOMs are used to organize and segregate managed devices and policies.

    Returns:
        Dictionary with list of ADOMs and their details

    Example:
        result = list_adoms()
    """
    try:
        client = get_fmg_client()
        if not client:
            raise RuntimeError("FortiManager client not initialized")

        api = ADOMAPI(client)
        adoms = await api.list_adoms()

        return {
            "status": "success",
            "count": len(adoms),
            "adoms": [
                {
                    "name": a.name,
                    "description": a.desc,
                    "os_version": a.os_ver,
                    "maintenance_release": a.mr,
                    "state": a.state,
                    "workspace_mode": a.workspace_mode,
                }
                for a in adoms
            ],
        }
    except Exception as e:
        logger.error(f"Error listing ADOMs: {e}")
        return {"status": "error", "message": str(e)}


# ============================================================================
# Phase 1: Basic Device Operations (NEW)
# ============================================================================

@mcp.tool()
async def add_real_device(
    name: str,
    ip: str,
    username: str,
    password: str,
    adom: str = "root",
    mgmt_mode: str = "fmg",
) -> dict[str, Any]:
    """Add a real (physical) FortiGate device to FortiManager.

    Adds an existing FortiGate device to FortiManager for management.
    This operation creates a task that can be monitored for completion.

    Args:
        name: Device name to use in FortiManager
        ip: IP address of the FortiGate device
        username: Admin username for the device
        password: Admin password for the device
        adom: ADOM to add the device to (default: "root")
        mgmt_mode: Management mode - "fmg" (FortiManager), "fmgfaz" (with FortiAnalyzer), or "unreg" (unregistered)

    Returns:
        Dictionary with task information

    Example:
        result = add_real_device(
            name="FGT-Branch-01",
            ip="10.1.1.1",
            username="admin",
            password="fortinet123",
            adom="root"
        )
    """
    try:
        api = _get_device_api()
        result = await api.add_real_device(
            name=name,
            ip=ip,
            username=username,
            password=password,
            adom=adom,
            mgmt_mode=mgmt_mode,
        )

        return {
            "status": "success",
            "message": f"Device '{name}' addition initiated",
            "task_info": result,
            "note": "Use monitoring tools to check task status",
        }
    except Exception as e:
        logger.error(f"Error adding real device '{name}': {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def rename_device(
    current_name: str,
    new_name: str,
    adom: str | None = None,
) -> dict[str, Any]:
    """Rename a managed device.

    Changes the name of a managed FortiGate device in FortiManager.

    Args:
        current_name: Current device name
        new_name: New device name
        adom: Optional ADOM name (None for global)

    Returns:
        Dictionary with rename result

    Example:
        result = rename_device(
            current_name="FGT-OLD-NAME",
            new_name="FGT-NEW-NAME",
            adom="root"
        )
    """
    try:
        api = _get_device_api()
        result = await api.rename_device(
            current_name=current_name,
            new_name=new_name,
            adom=adom,
        )

        return {
            "status": "success",
            "message": f"Device renamed from '{current_name}' to '{new_name}'",
            "result": result,
        }
    except Exception as e:
        logger.error(f"Error renaming device from '{current_name}' to '{new_name}': {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def refresh_device(device: str, adom: str = "root") -> dict[str, Any]:
    """Refresh device configuration from the managed FortiGate.

    Retrieves the latest configuration from the FortiGate device and
    updates FortiManager's database. This operation creates a task.

    Args:
        device: Device name
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with task information

    Example:
        result = refresh_device(device="FGT-Branch-01", adom="root")
    """
    try:
        api = _get_device_api()
        result = await api.refresh_device(device=device, adom=adom)

        return {
            "status": "success",
            "message": f"Device '{device}' refresh initiated",
            "task_info": result,
            "note": "Use monitoring tools to check task status",
        }
    except Exception as e:
        logger.error(f"Error refreshing device '{device}': {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_device_oid(device_name: str) -> dict[str, Any]:
    """Get the OID (Object ID) of a managed device.

    Retrieves the internal FortiManager Object ID for a device.
    The OID is used in some advanced API operations.

    Args:
        device_name: Device name

    Returns:
        Dictionary with device OID

    Example:
        result = get_device_oid(device_name="FGT-Branch-01")
    """
    try:
        api = _get_device_api()
        oid = await api.get_device_oid(device_name=device_name)

        return {
            "status": "success",
            "device_name": device_name,
            "oid": oid,
        }
    except Exception as e:
        logger.error(f"Error getting OID for device '{device_name}': {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_unauthorized_devices() -> dict[str, Any]:
    """Get list of unauthorized (unregistered) devices.

    Retrieves all devices that are visible to FortiManager but not yet
    authorized for management. These devices can be authorized using
    the authorize_device tool.

    Returns:
        Dictionary with list of unauthorized devices

    Example:
        result = get_unauthorized_devices()
    """
    try:
        api = _get_device_api()
        devices = await api.get_unauthorized_devices()

        return {
            "status": "success",
            "count": len(devices),
            "unauthorized_devices": devices,
            "note": "Use authorize_device tool to promote these devices",
        }
    except Exception as e:
        logger.error(f"Error getting unauthorized devices: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def authorize_device(
    device_name: str,
    username: str | None = None,
    password: str | None = None,
    adom: str = "root",
) -> dict[str, Any]:
    """Authorize (promote) an unauthorized device for management.

    Promotes an unauthorized device to a fully managed device.
    Credentials are optional if they were previously configured.

    Args:
        device_name: Device name (from unauthorized devices list)
        username: Admin username (optional if already configured)
        password: Admin password (optional if already configured)
        adom: ADOM to add the device to (default: "root")

    Returns:
        Dictionary with task information

    Example:
        # With credentials
        result = authorize_device(
            device_name="FGT-001",
            username="admin",
            password="fortinet123",
            adom="root"
        )

        # Without credentials (if already configured)
        result = authorize_device(device_name="FGT-001", adom="root")
    """
    try:
        api = _get_device_api()
        result = await api.authorize_device(
            device_name=device_name,
            username=username,
            password=password,
            adom=adom,
        )

        return {
            "status": "success",
            "message": f"Device '{device_name}' authorization initiated",
            "task_info": result,
            "note": "Use monitoring tools to check task status",
        }
    except Exception as e:
        logger.error(f"Error authorizing device '{device_name}': {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def change_device_serial_number(
    device_name: str,
    new_serial_number: str,
) -> dict[str, Any]:
    """Change the serial number of a managed device.

    Updates the serial number of a device in FortiManager.
    Useful when replacing hardware or fixing incorrect serial numbers.

    Args:
        device_name: Device name
        new_serial_number: New serial number

    Returns:
        Dictionary with update result

    Example:
        result = change_device_serial_number(
            device_name="FGT-Branch-01",
            new_serial_number="FGT60F1234567890"
        )
    """
    try:
        api = _get_device_api()
        result = await api.change_device_serial_number(
            device_name=device_name,
            new_serial_number=new_serial_number,
        )

        return {
            "status": "success",
            "message": f"Serial number changed for device '{device_name}'",
            "result": result,
        }
    except Exception as e:
        logger.error(f"Error changing serial number for device '{device_name}': {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_available_timezones() -> dict[str, Any]:
    """Get list of available timezones for device configuration.

    Retrieves all supported timezone values that can be used when
    configuring FortiGate devices.

    Returns:
        Dictionary with list of timezones

    Example:
        result = get_available_timezones()
    """
    try:
        api = _get_device_api()
        timezones = await api.get_available_timezones()

        return {
            "status": "success",
            "count": len(timezones),
            "timezones": timezones,
        }
    except Exception as e:
        logger.error(f"Error getting available timezones: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_full_device_db_syntax(adom: str = "root") -> dict[str, Any]:
    """Get the full device database syntax/schema.

    Retrieves the complete schema for the device database,
    showing all available fields and their types.

    Args:
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with device database syntax

    Example:
        result = get_full_device_db_syntax(adom="root")
    """
    try:
        api = _get_device_api()
        syntax = await api.get_full_device_db_syntax(adom=adom)

        return {
            "status": "success",
            "adom": adom,
            "syntax": syntax,
        }
    except Exception as e:
        logger.error(f"Error getting device DB syntax: {e}")
        return {"status": "error", "message": str(e)}


# ============================================================================
# Phase 2: Model Device Tools (NEW)
# ============================================================================

@mcp.tool()
async def get_supported_model_devices() -> dict[str, Any]:
    """Get list of supported model device platforms.

    Returns all FortiGate platforms that can be used to create model devices.

    Returns:
        Dictionary with list of supported platforms

    Example:
        result = get_supported_model_devices()
    """
    try:
        api = _get_device_api()
        platforms = await api.get_supported_model_devices()

        return {
            "status": "success",
            "count": len(platforms),
            "platforms": platforms,
        }
    except Exception as e:
        logger.error(f"Error getting supported model devices: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def create_model_device(
    name: str,
    platform: str,
    serial_number: str,
    adom: str = "root",
    os_ver: str = "7.0",
) -> dict[str, Any]:
    """Create a model (virtual) FortiGate device.

    Model devices are virtual devices used for planning, testing, or templates.
    They don't require actual hardware.

    Args:
        name: Device name
        platform: Platform string (e.g., "FortiGate-VM64", "FortiGate-60F")
        serial_number: Serial number for the model device
        adom: ADOM to add device to (default: "root")
        os_ver: OS version (default: "7.0")

    Returns:
        Dictionary with task information

    Example:
        result = create_model_device(
            name="MODEL-FGT-01",
            platform="FortiGate-VM64",
            serial_number="FGVM01234567890",
            adom="root"
        )
    """
    try:
        api = _get_device_api()
        result = await api.create_model_device(
            name=name,
            platform=platform,
            serial_number=serial_number,
            adom=adom,
            os_ver=os_ver,
        )

        return {
            "status": "success",
            "message": f"Model device '{name}' creation initiated",
            "task_info": result,
        }
    except Exception as e:
        logger.error(f"Error creating model device '{name}': {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def list_model_devices(adom: str | None = None) -> dict[str, Any]:
    """List model devices.

    Retrieves all model (virtual) devices, optionally filtered by ADOM.

    Args:
        adom: Optional ADOM name

    Returns:
        Dictionary with list of model devices

    Example:
        result = list_model_devices(adom="root")
    """
    try:
        api = _get_device_api()
        devices = await api.list_model_devices(adom=adom)

        return {
            "status": "success",
            "count": len(devices),
            "model_devices": devices,
        }
    except Exception as e:
        logger.error(f"Error listing model devices: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def enable_device_auto_link(
    device_name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Enable auto-link flag on a model device.

    Auto-link automatically links the model device to a real device
    when it comes online with the same serial number.

    Args:
        device_name: Device name
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with update result

    Example:
        result = enable_device_auto_link(
            device_name="MODEL-FGT-01",
            adom="root"
        )
    """
    try:
        api = _get_device_api()
        result = await api.enable_device_auto_link(
            device_name=device_name,
            adom=adom,
        )

        return {
            "status": "success",
            "message": f"Auto-link enabled for device '{device_name}'",
            "result": result,
        }
    except Exception as e:
        logger.error(f"Error enabling auto-link for device '{device_name}': {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def disable_device_auto_link(
    device_name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Disable auto-link flag on a model device.

    Args:
        device_name: Device name
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with update result

    Example:
        result = disable_device_auto_link(
            device_name="MODEL-FGT-01",
            adom="root"
        )
    """
    try:
        api = _get_device_api()
        result = await api.disable_device_auto_link(
            device_name=device_name,
            adom=adom,
        )

        return {
            "status": "success",
            "message": f"Auto-link disabled for device '{device_name}'",
            "result": result,
        }
    except Exception as e:
        logger.error(f"Error disabling auto-link for device '{device_name}': {e}")
        return {"status": "error", "message": str(e)}


# ============================================================================
# Phase 3: Device Group Tools (NEW)
# ============================================================================

@mcp.tool()
async def create_device_group(
    name: str,
    adom: str = "root",
    description: str | None = None,
) -> dict[str, Any]:
    """Create a device group.

    Device groups organize devices for easier management and bulk operations.

    Args:
        name: Group name
        adom: ADOM name (default: "root")
        description: Optional group description

    Returns:
        Dictionary with created group

    Example:
        result = create_device_group(
            name="branch-offices",
            adom="root",
            description="All branch office devices"
        )
    """
    try:
        api = _get_device_api()
        result = await api.create_device_group(
            name=name,
            adom=adom,
            description=description,
        )

        return {
            "status": "success",
            "message": f"Device group '{name}' created",
            "result": result,
        }
    except Exception as e:
        logger.error(f"Error creating device group '{name}': {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def list_device_groups(adom: str = "root") -> dict[str, Any]:
    """List all device groups.

    Args:
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with list of device groups

    Example:
        result = list_device_groups(adom="root")
    """
    try:
        api = _get_device_api()
        groups = await api.list_device_groups(adom=adom)

        return {
            "status": "success",
            "count": len(groups),
            "device_groups": groups,
        }
    except Exception as e:
        logger.error(f"Error listing device groups: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_device_group(
    group_name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Get device group details.

    Args:
        group_name: Group name
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with group details

    Example:
        result = get_device_group(group_name="branch-offices", adom="root")
    """
    try:
        api = _get_device_api()
        group = await api.get_device_group(
            group_name=group_name,
            adom=adom,
        )

        return {
            "status": "success",
            "device_group": group,
        }
    except Exception as e:
        logger.error(f"Error getting device group '{group_name}': {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def add_device_to_group(
    device_name: str,
    group_name: str,
    adom: str = "root",
    vdom: str = "root",
) -> dict[str, Any]:
    """Add a device to a device group.

    Args:
        device_name: Device name
        group_name: Group name
        adom: ADOM name (default: "root")
        vdom: VDOM name (default: "root")

    Returns:
        Dictionary with result

    Example:
        result = add_device_to_group(
            device_name="FGT-Branch-01",
            group_name="branch-offices",
            adom="root"
        )
    """
    try:
        api = _get_device_api()
        result = await api.add_device_to_group(
            device_name=device_name,
            group_name=group_name,
            adom=adom,
            vdom=vdom,
        )

        return {
            "status": "success",
            "message": f"Device '{device_name}' added to group '{group_name}'",
            "result": result,
        }
    except Exception as e:
        logger.error(f"Error adding device '{device_name}' to group '{group_name}': {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def remove_device_from_group(
    device_name: str,
    group_name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Remove a device from a device group.

    Args:
        device_name: Device name
        group_name: Group name
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with result

    Example:
        result = remove_device_from_group(
            device_name="FGT-Branch-01",
            group_name="branch-offices",
            adom="root"
        )
    """
    try:
        api = _get_device_api()
        result = await api.remove_device_from_group(
            device_name=device_name,
            group_name=group_name,
            adom=adom,
        )

        return {
            "status": "success",
            "message": f"Device '{device_name}' removed from group '{group_name}'",
            "result": result,
        }
    except Exception as e:
        logger.error(f"Error removing device '{device_name}' from group '{group_name}': {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def delete_device_group(
    group_name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Delete a device group.

    Args:
        group_name: Group name
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with result

    Example:
        result = delete_device_group(group_name="branch-offices", adom="root")
    """
    try:
        api = _get_device_api()
        result = await api.delete_device_group(
            group_name=group_name,
            adom=adom,
        )

        return {
            "status": "success",
            "message": f"Device group '{group_name}' deleted",
            "result": result,
        }
    except Exception as e:
        logger.error(f"Error deleting device group '{group_name}': {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_device_group_members(
    group_name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Get members of a device group.

    Args:
        group_name: Group name
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with list of group members

    Example:
        result = get_device_group_members(group_name="branch-offices", adom="root")
    """
    try:
        api = _get_device_api()
        members = await api.get_device_group_members(
            group_name=group_name,
            adom=adom,
        )

        return {
            "status": "success",
            "group_name": group_name,
            "count": len(members),
            "members": members,
        }
    except Exception as e:
        logger.error(f"Error getting members of device group '{group_name}': {e}")
        return {"status": "error", "message": str(e)}


# ============================================================================
# Phase 4: VDOM Tools (NEW)
# ============================================================================

@mcp.tool()
async def enable_vdom(
    device_name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Enable VDOM mode on a device.

    Enables multi-VDOM mode on a FortiGate device, allowing multiple
    virtual domains for multi-tenancy.

    Args:
        device_name: Device name
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with result

    Example:
        result = enable_vdom(device_name="FGT-Branch-01", adom="root")
    """
    try:
        api = _get_device_api()
        result = await api.enable_vdom(
            device_name=device_name,
            adom=adom,
        )

        return {
            "status": "success",
            "message": f"VDOM mode enabled on device '{device_name}'",
            "result": result,
            "note": "Device may require reboot to apply changes",
        }
    except Exception as e:
        logger.error(f"Error enabling VDOM on device '{device_name}': {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def add_vdom(
    device_name: str,
    vdom_name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Add a VDOM to a device.

    Creates a new Virtual Domain on a FortiGate device.

    Args:
        device_name: Device name
        vdom_name: VDOM name to create
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with created VDOM

    Example:
        result = add_vdom(
            device_name="FGT-Branch-01",
            vdom_name="customer1",
            adom="root"
        )
    """
    try:
        api = _get_device_api()
        result = await api.add_vdom(
            device_name=device_name,
            vdom_name=vdom_name,
            adom=adom,
        )

        return {
            "status": "success",
            "message": f"VDOM '{vdom_name}' created on device '{device_name}'",
            "result": result,
        }
    except Exception as e:
        logger.error(f"Error adding VDOM '{vdom_name}' to device '{device_name}': {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def delete_vdom(
    device_name: str,
    vdom_name: str,
) -> dict[str, Any]:
    """Delete a VDOM from a device.

    Args:
        device_name: Device name
        vdom_name: VDOM name to delete

    Returns:
        Dictionary with result

    Example:
        result = delete_vdom(device_name="FGT-Branch-01", vdom_name="customer1")
    """
    try:
        api = _get_device_api()
        result = await api.delete_vdom(
            device_name=device_name,
            vdom_name=vdom_name,
        )

        return {
            "status": "success",
            "message": f"VDOM '{vdom_name}' deleted from device '{device_name}'",
            "result": result,
        }
    except Exception as e:
        logger.error(f"Error deleting VDOM '{vdom_name}' from device '{device_name}': {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def list_device_vdoms(
    device_name: str,
    adom: str | None = None,
) -> dict[str, Any]:
    """List VDOMs for a device.

    Args:
        device_name: Device name
        adom: Optional ADOM name

    Returns:
        Dictionary with list of VDOMs

    Example:
        result = list_device_vdoms(device_name="FGT-Branch-01", adom="root")
    """
    try:
        api = _get_device_api()
        vdoms = await api.list_device_vdoms(
            device_name=device_name,
            adom=adom,
        )

        return {
            "status": "success",
            "device_name": device_name,
            "count": len(vdoms),
            "vdoms": vdoms,
        }
    except Exception as e:
        logger.error(f"Error listing VDOMs for device '{device_name}': {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def assign_vdom_to_adom(
    device_name: str,
    vdom_name: str,
    target_adom: str,
    source_adom: str = "root",
) -> dict[str, Any]:
    """Assign a VDOM to a different ADOM.

    Moves a VDOM from one ADOM to another for multi-tenant scenarios.

    Args:
        device_name: Device name
        vdom_name: VDOM name
        target_adom: Target ADOM to assign to
        source_adom: Source ADOM (default: "root")

    Returns:
        Dictionary with assignment result

    Example:
        result = assign_vdom_to_adom(
            device_name="FGT-Branch-01",
            vdom_name="customer1",
            target_adom="customer1-adom",
            source_adom="root"
        )
    """
    try:
        api = _get_device_api()
        result = await api.assign_vdom_to_adom(
            device_name=device_name,
            vdom_name=vdom_name,
            target_adom=target_adom,
            source_adom=source_adom,
        )

        return {
            "status": "success",
            "message": f"VDOM '{vdom_name}' assigned to ADOM '{target_adom}'",
            "result": result,
        }
    except Exception as e:
        logger.error(f"Error assigning VDOM '{vdom_name}' to ADOM '{target_adom}': {e}")
        return {"status": "error", "message": str(e)}


# ============================================================================
# Phase 5: Firmware Management Tools (NEW)
# ============================================================================

@mcp.tool()
async def get_upgrade_path(
    device_name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Get the firmware upgrade path for a device.

    Shows available firmware upgrade options and recommendations for a device.

    Args:
        device_name: Device name
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with upgrade path information

    Example:
        result = get_upgrade_path(device_name="FGT-Branch-01", adom="root")
    """
    try:
        api = _get_device_api()
        result = await api.get_upgrade_path(
            device_name=device_name,
            adom=adom,
        )

        return {
            "status": "success",
            "device": device_name,
            "upgrade_path": result,
        }
    except Exception as e:
        logger.error(f"Error getting upgrade path for device '{device_name}': {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def list_available_firmware(
    platform: str | None = None,
) -> dict[str, Any]:
    """List firmware images available on FortiManager.

    Args:
        platform: Optional platform filter (e.g., "FortiGate-VM64")

    Returns:
        Dictionary with list of firmware images

    Example:
        # List all firmware
        result = list_available_firmware()

        # List for specific platform
        result = list_available_firmware(platform="FortiGate-VM64")
    """
    try:
        api = _get_device_api()
        firmware = await api.list_available_firmware(platform=platform)

        return {
            "status": "success",
            "platform": platform or "all",
            "count": len(firmware),
            "firmware": firmware,
        }
    except Exception as e:
        logger.error(f"Error listing available firmware: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def upgrade_device_firmware(
    device_name: str,
    image: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Upgrade a device to a specific firmware version.

    WARNING: This operation will upgrade device firmware and may cause downtime.

    Args:
        device_name: Device name
        image: Firmware image path (from list_available_firmware)
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with upgrade task information

    Example:
        result = upgrade_device_firmware(
            device_name="FGT-Branch-01",
            image="FGT_VM64-v7.0.12-build0523-FORTINET.out",
            adom="root"
        )
    """
    try:
        api = _get_device_api()
        result = await api.upgrade_device(
            device_name=device_name,
            image=image,
            adom=adom,
        )

        return {
            "status": "success",
            "message": f"Firmware upgrade initiated for device '{device_name}'",
            "task_info": result,
            "note": "Use monitoring tools to check upgrade progress",
        }
    except Exception as e:
        logger.error(f"Error upgrading device '{device_name}': {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_upgrade_history(
    device_name: str | None = None,
    adom: str = "root",
) -> dict[str, Any]:
    """Get firmware upgrade history.

    Args:
        device_name: Optional device name filter
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with upgrade history

    Example:
        # All upgrades
        result = get_upgrade_history(adom="root")

        # Specific device
        result = get_upgrade_history(device_name="FGT-Branch-01", adom="root")
    """
    try:
        api = _get_device_api()
        history = await api.get_upgrade_history(
            device_name=device_name,
            adom=adom,
        )

        return {
            "status": "success",
            "device": device_name or "all",
            "count": len(history),
            "upgrade_history": history,
        }
    except Exception as e:
        logger.error(f"Error getting upgrade history: {e}")
        return {"status": "error", "message": str(e)}


# ============================================================================
# Phase 6: Device Revision Tools (NEW)
# ============================================================================

@mcp.tool()
async def list_device_revisions(
    device_name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """List device configuration revisions.

    Shows all saved configuration revisions for a device.

    Args:
        device_name: Device name
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with list of revisions

    Example:
        result = list_device_revisions(device_name="FGT-Branch-01", adom="root")
    """
    try:
        api = _get_device_api()
        revisions = await api.list_device_revisions(
            device_name=device_name,
            adom=adom,
        )

        return {
            "status": "success",
            "device": device_name,
            "count": len(revisions),
            "revisions": revisions,
        }
    except Exception as e:
        logger.error(f"Error listing revisions for device '{device_name}': {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_device_revision(
    device_name: str,
    revision_id: int,
    adom: str = "root",
) -> dict[str, Any]:
    """Get a specific device configuration revision.

    Args:
        device_name: Device name
        revision_id: Revision ID
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with revision details

    Example:
        result = get_device_revision(
            device_name="FGT-Branch-01",
            revision_id=5,
            adom="root"
        )
    """
    try:
        api = _get_device_api()
        revision = await api.get_device_revision(
            device_name=device_name,
            revision_id=revision_id,
            adom=adom,
        )

        return {
            "status": "success",
            "device": device_name,
            "revision_id": revision_id,
            "revision": revision,
        }
    except Exception as e:
        logger.error(f"Error getting revision {revision_id} for device '{device_name}': {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_current_device_config(
    device_name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Get current device database configuration.

    Args:
        device_name: Device name
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with current configuration

    Example:
        result = get_current_device_config(device_name="FGT-Branch-01", adom="root")
    """
    try:
        api = _get_device_api()
        config = await api.get_current_device_config(
            device_name=device_name,
            adom=adom,
        )

        return {
            "status": "success",
            "device": device_name,
            "configuration": config,
        }
    except Exception as e:
        logger.error(f"Error getting current config for device '{device_name}': {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def revert_device_revision(
    device_name: str,
    revision_id: int,
    adom: str = "root",
) -> dict[str, Any]:
    """Revert device to a specific configuration revision.

    WARNING: This operation will change the device configuration.

    Args:
        device_name: Device name
        revision_id: Revision ID to revert to
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with revert result

    Example:
        result = revert_device_revision(
            device_name="FGT-Branch-01",
            revision_id=5,
            adom="root"
        )
    """
    try:
        api = _get_device_api()
        result = await api.revert_device_revision(
            device_name=device_name,
            revision_id=revision_id,
            adom=adom,
        )

        return {
            "status": "success",
            "message": f"Device '{device_name}' reverted to revision {revision_id}",
            "result": result,
        }
    except Exception as e:
        logger.error(f"Error reverting device '{device_name}' to revision {revision_id}: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def retrieve_device_config(
    device_name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Retrieve latest configuration from the device.

    Triggers a retrieve operation to pull the latest config from the FortiGate.

    Args:
        device_name: Device name
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with task information

    Example:
        result = retrieve_device_config(device_name="FGT-Branch-01", adom="root")
    """
    try:
        api = _get_device_api()
        result = await api.retrieve_device_config(
            device_name=device_name,
            adom=adom,
        )

        return {
            "status": "success",
            "message": f"Config retrieve initiated for device '{device_name}'",
            "task_info": result,
        }
    except Exception as e:
        logger.error(f"Error retrieving config for device '{device_name}': {e}")
        return {"status": "error", "message": str(e)}


# ============================================================================
# Phase 7: HA Cluster Tools (NEW)
# ============================================================================

@mcp.tool()
async def create_ha_cluster(
    name: str,
    platform: str,
    primary_sn: str,
    secondary_sn: str,
    adom: str = "root",
    os_ver: str = "7.0",
) -> dict[str, Any]:
    """Create a Model HA Cluster.

    Creates a virtual HA cluster with primary and secondary devices.

    Args:
        name: Cluster name
        platform: Platform string (e.g., "FortiGate-VM64")
        primary_sn: Primary device serial number
        secondary_sn: Secondary device serial number
        adom: ADOM name (default: "root")
        os_ver: OS version (default: "7.0")

    Returns:
        Dictionary with task information

    Example:
        result = create_ha_cluster(
            name="HA-Cluster-01",
            platform="FortiGate-VM64",
            primary_sn="FGVM010000000001",
            secondary_sn="FGVM010000000002",
            adom="root"
        )
    """
    try:
        api = _get_device_api()
        result = await api.create_ha_cluster(
            name=name,
            platform=platform,
            primary_sn=primary_sn,
            secondary_sn=secondary_sn,
            adom=adom,
            os_ver=os_ver,
        )

        return {
            "status": "success",
            "message": f"HA cluster '{name}' creation initiated",
            "task_info": result,
        }
    except Exception as e:
        logger.error(f"Error creating HA cluster '{name}': {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_cluster_members(
    cluster_name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Get HA cluster member information.

    Args:
        cluster_name: Cluster name
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with cluster members

    Example:
        result = get_cluster_members(cluster_name="HA-Cluster-01", adom="root")
    """
    try:
        api = _get_device_api()
        members = await api.get_cluster_members(
            cluster_name=cluster_name,
            adom=adom,
        )

        return {
            "status": "success",
            "cluster": cluster_name,
            "count": len(members),
            "members": members,
        }
    except Exception as e:
        logger.error(f"Error getting members of cluster '{cluster_name}': {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def failover_cluster(
    cluster_name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Trigger a failover for an HA cluster.

    WARNING: This operation will trigger an HA failover.

    Args:
        cluster_name: Cluster name
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with failover result

    Example:
        result = failover_cluster(cluster_name="HA-Cluster-01", adom="root")
    """
    try:
        api = _get_device_api()
        result = await api.failover_cluster(
            cluster_name=cluster_name,
            adom=adom,
        )

        return {
            "status": "success",
            "message": f"Failover triggered for cluster '{cluster_name}'",
            "result": result,
        }
    except Exception as e:
        logger.error(f"Error failing over cluster '{cluster_name}': {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def update_cluster_serial_numbers(
    cluster_name: str,
    primary_sn: str,
    secondary_sn: str | None = None,
    adom: str = "root",
) -> dict[str, Any]:
    """Update/replace serial numbers of HA cluster members.

    Useful when replacing hardware or fixing incorrect serial numbers.

    Args:
        cluster_name: Cluster name
        primary_sn: New primary device serial number
        secondary_sn: New secondary device serial number (optional)
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with update result

    Example:
        result = update_cluster_serial_numbers(
            cluster_name="HA-Cluster-01",
            primary_sn="FGVM010000000003",
            secondary_sn="FGVM010000000004",
            adom="root"
        )
    """
    try:
        api = _get_device_api()
        result = await api.update_cluster_serial_numbers(
            cluster_name=cluster_name,
            primary_sn=primary_sn,
            secondary_sn=secondary_sn,
            adom=adom,
        )

        return {
            "status": "success",
            "message": f"Serial numbers updated for cluster '{cluster_name}'",
            "result": result,
        }
    except Exception as e:
        logger.error(f"Error updating serial numbers for cluster '{cluster_name}': {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_cluster_status(
    cluster_name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Get HA cluster members status.

    Args:
        cluster_name: Cluster name
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with cluster status

    Example:
        result = get_cluster_status(cluster_name="HA-Cluster-01", adom="root")
    """
    try:
        api = _get_device_api()
        status = await api.get_cluster_status(
            cluster_name=cluster_name,
            adom=adom,
        )

        return {
            "status": "success",
            "cluster": cluster_name,
            "cluster_status": status,
        }
    except Exception as e:
        logger.error(f"Error getting status of cluster '{cluster_name}': {e}")
        return {"status": "error", "message": str(e)}


# ============================================================================
# Phase 8: Device Metadata & Blueprint Tools (NEW)
# ============================================================================

@mcp.tool()
async def get_device_meta_fields(
    device_name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Get device meta fields.

    Meta fields store custom metadata about devices.

    Args:
        device_name: Device name
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with device meta fields

    Example:
        result = get_device_meta_fields(device_name="FGT-Branch-01", adom="root")
    """
    try:
        api = _get_device_api()
        meta_fields = await api.get_device_meta_fields(
            device_name=device_name,
            adom=adom,
        )

        return {
            "status": "success",
            "device": device_name,
            "meta_fields": meta_fields,
        }
    except Exception as e:
        logger.error(f"Error getting meta fields for device '{device_name}': {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def set_device_meta_fields(
    device_name: str,
    meta_fields: dict[str, Any],
    adom: str = "root",
) -> dict[str, Any]:
    """Set device meta fields.

    Args:
        device_name: Device name
        meta_fields: Meta fields to set (dictionary)
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with result

    Example:
        result = set_device_meta_fields(
            device_name="FGT-Branch-01",
            meta_fields={"location": "Building A", "contact": "admin@company.com"},
            adom="root"
        )
    """
    try:
        api = _get_device_api()
        result = await api.set_device_meta_fields(
            device_name=device_name,
            meta_fields=meta_fields,
            adom=adom,
        )

        return {
            "status": "success",
            "message": f"Meta fields set for device '{device_name}'",
            "result": result,
        }
    except Exception as e:
        logger.error(f"Error setting meta fields for device '{device_name}': {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_vdom_meta_fields(
    device_name: str,
    vdom_name: str | None = None,
    adom: str = "root",
) -> dict[str, Any]:
    """Get VDOM meta fields.

    Args:
        device_name: Device name
        vdom_name: Optional VDOM name (None for all VDOMs)
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with VDOM meta fields

    Example:
        # Get all VDOMs meta fields
        result = get_vdom_meta_fields(device_name="FGT-Branch-01", adom="root")

        # Get specific VDOM meta fields
        result = get_vdom_meta_fields(device_name="FGT-Branch-01", vdom_name="customer1", adom="root")
    """
    try:
        api = _get_device_api()
        meta_fields = await api.get_vdom_meta_fields(
            device_name=device_name,
            vdom_name=vdom_name,
            adom=adom,
        )

        return {
            "status": "success",
            "device": device_name,
            "vdom": vdom_name or "all",
            "meta_fields": meta_fields,
        }
    except Exception as e:
        logger.error(f"Error getting VDOM meta fields for device '{device_name}': {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def set_vdom_meta_fields(
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
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with result

    Example:
        result = set_vdom_meta_fields(
            device_name="FGT-Branch-01",
            vdom_name="customer1",
            meta_fields={"tenant": "Customer 1", "billing_code": "CUST001"},
            adom="root"
        )
    """
    try:
        api = _get_device_api()
        result = await api.set_vdom_meta_fields(
            device_name=device_name,
            vdom_name=vdom_name,
            meta_fields=meta_fields,
            adom=adom,
        )

        return {
            "status": "success",
            "message": f"Meta fields set for VDOM '{vdom_name}' on device '{device_name}'",
            "result": result,
        }
    except Exception as e:
        logger.error(f"Error setting VDOM meta fields: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def list_device_blueprints(adom: str = "root") -> dict[str, Any]:
    """List device blueprints.

    Device blueprints define standard configurations for devices.

    Args:
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with list of blueprints

    Example:
        result = list_device_blueprints(adom="root")
    """
    try:
        api = _get_device_api()
        blueprints = await api.list_device_blueprints(adom=adom)

        return {
            "status": "success",
            "count": len(blueprints),
            "blueprints": blueprints,
        }
    except Exception as e:
        logger.error(f"Error listing device blueprints: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def create_device_blueprint(
    name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Create a device blueprint.

    Args:
        name: Blueprint name
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with created blueprint

    Example:
        result = create_device_blueprint(name="branch-template", adom="root")
    """
    try:
        api = _get_device_api()
        result = await api.create_device_blueprint(
            name=name,
            adom=adom,
        )

        return {
            "status": "success",
            "message": f"Device blueprint '{name}' created",
            "result": result,
        }
    except Exception as e:
        logger.error(f"Error creating device blueprint '{name}': {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def delete_device_blueprint(
    blueprint_name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Delete a device blueprint.

    Args:
        blueprint_name: Blueprint name
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with result

    Example:
        result = delete_device_blueprint(blueprint_name="branch-template", adom="root")
    """
    try:
        api = _get_device_api()
        result = await api.delete_device_blueprint(
            blueprint_name=blueprint_name,
            adom=adom,
        )

        return {
            "status": "success",
            "message": f"Device blueprint '{blueprint_name}' deleted",
            "result": result,
        }
    except Exception as e:
        logger.error(f"Error deleting device blueprint '{blueprint_name}': {e}")
        return {"status": "error", "message": str(e)}


# ============================================================================
# Phase 9: Network Settings Tools (NEW)
# ============================================================================

@mcp.tool()
async def add_vlan_interface(
    device_name: str,
    interface: str,
    vlan_id: int,
    vdom: str = "root",
) -> dict[str, Any]:
    """Add a VLAN interface to a device.

    Args:
        device_name: Device name
        interface: Physical interface name (e.g., "port1")
        vlan_id: VLAN ID (1-4094)
        vdom: VDOM name (default: "root")

    Returns:
        Dictionary with result

    Example:
        result = add_vlan_interface(
            device_name="FGT-Branch-01",
            interface="port1",
            vlan_id=100,
            vdom="root"
        )
    """
    try:
        api = _get_device_api()
        result = await api.add_vlan(
            device_name=device_name,
            interface=interface,
            vlan_id=vlan_id,
            vdom=vdom,
        )

        return {
            "status": "success",
            "message": f"VLAN {vlan_id} added to interface {interface}",
            "result": result,
        }
    except Exception as e:
        logger.error(f"Error adding VLAN interface: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def add_interface_to_zone(
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
        vdom: VDOM name (default: "root")

    Returns:
        Dictionary with result

    Example:
        result = add_interface_to_zone(
            device_name="FGT-Branch-01",
            zone_name="LAN",
            interface="port2",
            vdom="root"
        )
    """
    try:
        api = _get_device_api()
        result = await api.add_zone_member(
            device_name=device_name,
            zone_name=zone_name,
            interface=interface,
            vdom=vdom,
        )

        return {
            "status": "success",
            "message": f"Interface '{interface}' added to zone '{zone_name}'",
            "result": result,
        }
    except Exception as e:
        logger.error(f"Error adding interface to zone: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def remove_interface_from_zone(
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
        vdom: VDOM name (default: "root")

    Returns:
        Dictionary with result

    Example:
        result = remove_interface_from_zone(
            device_name="FGT-Branch-01",
            zone_name="LAN",
            interface="port2",
            vdom="root"
        )
    """
    try:
        api = _get_device_api()
        result = await api.delete_zone_member(
            device_name=device_name,
            zone_name=zone_name,
            interface=interface,
            vdom=vdom,
        )

        return {
            "status": "success",
            "message": f"Interface '{interface}' removed from zone '{zone_name}'",
            "result": result,
        }
    except Exception as e:
        logger.error(f"Error removing interface from zone: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def add_ospf_network_entry(
    device_name: str,
    network: str,
    area: str,
    vdom: str = "root",
) -> dict[str, Any]:
    """Add OSPF network entry.

    Args:
        device_name: Device name
        network: Network address with mask (e.g., "10.0.0.0 255.255.255.0")
        area: OSPF area ID
        vdom: VDOM name (default: "root")

    Returns:
        Dictionary with result

    Example:
        result = add_ospf_network_entry(
            device_name="FGT-Branch-01",
            network="10.0.1.0 255.255.255.0",
            area="0.0.0.0",
            vdom="root"
        )
    """
    try:
        api = _get_device_api()
        result = await api.add_ospf_network(
            device_name=device_name,
            network=network,
            area=area,
            vdom=vdom,
        )

        return {
            "status": "success",
            "message": f"OSPF network '{network}' added to area '{area}'",
            "result": result,
        }
    except Exception as e:
        logger.error(f"Error adding OSPF network: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_lte_modem_status(
    device_name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Get LTE modem status for a device.

    Args:
        device_name: Device name
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with LTE modem status

    Example:
        result = get_lte_modem_status(device_name="FGT-Branch-01", adom="root")
    """
    try:
        api = _get_device_api()
        status = await api.get_lte_modem_status(
            device_name=device_name,
            adom=adom,
        )

        return {
            "status": "success",
            "device": device_name,
            "lte_status": status,
        }
    except Exception as e:
        logger.error(f"Error getting LTE modem status for device '{device_name}': {e}")
        return {"status": "error", "message": str(e)}


# ============================================================================
# Phase 10: Advanced Operations Tools (NEW)
# ============================================================================

@mcp.tool()
async def upload_device_certificate(
    device_name: str,
    cert_name: str,
    cert_content: str,
    vdom: str = "root",
) -> dict[str, Any]:
    """Upload a certificate to a device.

    Args:
        device_name: Device name
        cert_name: Certificate name
        cert_content: Certificate content (PEM format)
        vdom: VDOM name (default: "root")

    Returns:
        Dictionary with result

    Example:
        result = upload_device_certificate(
            device_name="FGT-Branch-01",
            cert_name="server-cert",
            cert_content="-----BEGIN CERTIFICATE-----...",
            vdom="root"
        )
    """
    try:
        api = _get_device_api()
        result = await api.upload_certificate(
            device_name=device_name,
            cert_name=cert_name,
            cert_content=cert_content,
            vdom=vdom,
        )

        return {
            "status": "success",
            "message": f"Certificate '{cert_name}' uploaded to device '{device_name}'",
            "result": result,
        }
    except Exception as e:
        logger.error(f"Error uploading certificate: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_device_certificate_details(
    device_name: str,
    cert_name: str,
    vdom: str = "root",
) -> dict[str, Any]:
    """Get certificate details from a device.

    Args:
        device_name: Device name
        cert_name: Certificate name
        vdom: VDOM name (default: "root")

    Returns:
        Dictionary with certificate details

    Example:
        result = get_device_certificate_details(
            device_name="FGT-Branch-01",
            cert_name="server-cert",
            vdom="root"
        )
    """
    try:
        api = _get_device_api()
        cert = await api.get_certificate_details(
            device_name=device_name,
            cert_name=cert_name,
            vdom=vdom,
        )

        return {
            "status": "success",
            "device": device_name,
            "certificate": cert,
        }
    except Exception as e:
        logger.error(f"Error getting certificate details: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_install_preview(
    devices: list[str] | str,
    adom: str = "root",
    vdom: str = "root",
) -> dict[str, Any]:
    """Get install preview for device(s).

    Shows what changes will be made before installing.

    Args:
        devices: Device name or list of device names
        adom: ADOM name (default: "root")
        vdom: VDOM name (default: "root")

    Returns:
        Dictionary with install preview

    Example:
        # Single device
        result = get_install_preview(devices="FGT-Branch-01", adom="root")

        # Multiple devices
        result = get_install_preview(devices=["FGT-Branch-01", "FGT-Branch-02"], adom="root")
    """
    try:
        api = _get_device_api()
        preview = await api.get_install_preview(
            devices=devices,
            adom=adom,
            vdom=vdom,
        )

        return {
            "status": "success",
            "devices": devices if isinstance(devices, list) else [devices],
            "preview": preview,
        }
    except Exception as e:
        logger.error(f"Error getting install preview: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_vpn_tunnel_status(
    device_name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Get VPN tunnel status/details for a device.

    Args:
        device_name: Device name
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with VPN tunnel details

    Example:
        result = get_vpn_tunnel_status(device_name="FGT-Branch-01", adom="root")
    """
    try:
        api = _get_device_api()
        tunnels = await api.get_vpn_tunnel_details(
            device_name=device_name,
            adom=adom,
        )

        return {
            "status": "success",
            "device": device_name,
            "count": len(tunnels),
            "tunnels": tunnels,
        }
    except Exception as e:
        logger.error(f"Error getting VPN tunnel status for device '{device_name}': {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def set_device_rma_status(
    device_name: str,
    rma_status: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Set RMA status on a device.

    Args:
        device_name: Device name
        rma_status: RMA status value
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with result

    Example:
        result = set_device_rma_status(
            device_name="FGT-Branch-01",
            rma_status="pending",
            adom="root"
        )
    """
    try:
        api = _get_device_api()
        result = await api.set_rma_status(
            device_name=device_name,
            status=rma_status,
            adom=adom,
        )

        return {
            "status": "success",
            "message": f"RMA status set for device '{device_name}'",
            "result": result,
        }
    except Exception as e:
        logger.error(f"Error setting RMA status for device '{device_name}': {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_device_rma_status(
    device_name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Get RMA status of a device.

    Args:
        device_name: Device name
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with RMA status

    Example:
        result = get_device_rma_status(device_name="FGT-Branch-01", adom="root")
    """
    try:
        api = _get_device_api()
        rma_info = await api.get_rma_status(
            device_name=device_name,
            adom=adom,
        )

        return {
            "status": "success",
            "device": device_name,
            "rma_status": rma_info.get("rma_status"),
        }
    except Exception as e:
        logger.error(f"Error getting RMA status for device '{device_name}': {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_device_vulnerabilities(
    device_name: str | None = None,
    adom: str = "root",
) -> dict[str, Any]:
    """Get Fortinet vulnerabilities for managed devices.

    Args:
        device_name: Optional device name filter (None for all devices)
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with vulnerabilities

    Example:
        # All devices
        result = get_device_vulnerabilities(adom="root")

        # Specific device
        result = get_device_vulnerabilities(device_name="FGT-Branch-01", adom="root")
    """
    try:
        api = _get_device_api()
        vulns = await api.get_device_vulnerabilities(
            device_name=device_name,
            adom=adom,
        )

        return {
            "status": "success",
            "device": device_name or "all",
            "count": len(vulns),
            "vulnerabilities": vulns,
        }
    except Exception as e:
        logger.error(f"Error getting device vulnerabilities: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def run_device_cli_commands(
    device_name: str,
    commands: list[str],
    adom: str = "root",
) -> dict[str, Any]:
    """Run CLI commands against a managed device.

    WARNING: This executes commands directly on the device.

    Args:
        device_name: Device name
        commands: List of CLI commands to execute
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with command results

    Example:
        result = run_device_cli_commands(
            device_name="FGT-Branch-01",
            commands=["get system status", "diagnose hardware deviceinfo disk"],
            adom="root"
        )
    """
    try:
        api = _get_device_api()
        result = await api.run_cli_commands(
            device_name=device_name,
            commands=commands,
            adom=adom,
        )

        return {
            "status": "success",
            "device": device_name,
            "command_count": len(commands),
            "results": result,
        }
    except Exception as e:
        logger.error(f"Error running CLI commands on device '{device_name}': {e}")
        return {"status": "error", "message": str(e)}


# =============================================================================
# Phase 44: Additional Device Query Operations
# =============================================================================


@mcp.tool()
async def get_device_ha_configuration(device_name: str, adom: str = "root") -> dict[str, Any]:
    """Get device HA (High Availability) status and configuration.
    
    Args:
        device_name: Device name
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with HA status information
    """
    try:
        api = _get_device_api()
        ha_status = await api.get_device_ha_status(device_name=device_name, adom=adom)
        return {"status": "success", "ha_status": ha_status}
    except Exception as e:
        logger.error(f"Error getting device HA status: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_device_interface_configuration(device_name: str, adom: str = "root") -> dict[str, Any]:
    """Get list of device network interfaces.
    
    Args:
        device_name: Device name
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with list of interfaces
    """
    try:
        api = _get_device_api()
        interfaces = await api.get_device_interface_list(device_name=device_name, adom=adom)
        return {"status": "success", "count": len(interfaces), "interfaces": interfaces}
    except Exception as e:
        logger.error(f"Error getting device interfaces: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_device_routing_configuration(device_name: str, adom: str = "root") -> dict[str, Any]:
    """Get device routing table configuration.
    
    Args:
        device_name: Device name
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with routing table entries
    """
    try:
        api = _get_device_api()
        routes = await api.get_device_routing_table(device_name=device_name, adom=adom)
        return {"status": "success", "count": len(routes), "routes": routes}
    except Exception as e:
        logger.error(f"Error getting device routing table: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_device_vpn_monitoring(device_name: str, adom: str = "root") -> dict[str, Any]:
    """Get device VPN tunnel monitoring information.
    
    Args:
        device_name: Device name
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with VPN monitoring data
    """
    try:
        api = _get_device_api()
        vpn_monitor = await api.get_device_vpn_monitor(device_name=device_name, adom=adom)
        return {"status": "success", "vpn_monitor": vpn_monitor}
    except Exception as e:
        logger.error(f"Error getting device VPN monitoring: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_device_system_information(device_name: str, adom: str = "root") -> dict[str, Any]:
    """Get detailed device system status.
    
    Args:
        device_name: Device name
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with system status information
    """
    try:
        api = _get_device_api()
        system_status = await api.get_device_system_status(device_name=device_name, adom=adom)
        return {"status": "success", "system_status": system_status}
    except Exception as e:
        logger.error(f"Error getting device system status: {e}")
        return {"status": "error", "message": str(e)}

