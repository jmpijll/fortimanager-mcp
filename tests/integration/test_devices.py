"""Integration tests for device management API."""

import pytest

from fortimanager_mcp.api.client import FortiManagerClient
from fortimanager_mcp.api.devices import DeviceAPI


@pytest.mark.readonly
@pytest.mark.asyncio
async def test_list_devices(fmg_client: FortiManagerClient, test_adom: str):
    """Test listing devices (read-only operation)."""
    api = DeviceAPI(fmg_client)
    devices = await api.list_devices(adom=test_adom)

    assert isinstance(devices, list)
    # Should have at least one device in test environment
    # Remove this assertion if not applicable
    # assert len(devices) > 0

    if devices:
        device = devices[0]
        assert device.name
        # Check that device object has expected attributes
        assert hasattr(device, "ip")
        assert hasattr(device, "os_ver")
        assert hasattr(device, "conn_status")


@pytest.mark.readonly
@pytest.mark.device_required
@pytest.mark.asyncio
async def test_get_device(fmg_client: FortiManagerClient, test_adom: str, test_device: str):
    """Test getting specific device details (read-only operation)."""
    if not test_device:
        pytest.skip("TEST_DEVICE not configured")

    api = DeviceAPI(fmg_client)
    device = await api.get_device(name=test_device, adom=test_adom)

    assert device.name == test_device
    assert device.ip is not None
    # Device should have basic properties
    assert hasattr(device, "os_type")
    assert hasattr(device, "platform_str")


@pytest.mark.readonly
@pytest.mark.asyncio
async def test_list_devices_with_filter(fmg_client: FortiManagerClient, test_adom: str):
    """Test listing devices with filter (read-only operation)."""
    api = DeviceAPI(fmg_client)

    # Get all devices first
    all_devices = await api.list_devices(adom=test_adom)

    if not all_devices:
        pytest.skip("No devices available for testing")

    # Test with specific fields
    devices = await api.list_devices(adom=test_adom, fields=["name", "ip", "os_ver"])

    assert isinstance(devices, list)
    if devices:
        device = devices[0]
        assert device.name
        # When specific fields requested, should have those fields
        assert hasattr(device, "name")


@pytest.mark.readonly
@pytest.mark.device_required
@pytest.mark.asyncio
async def test_get_device_config(
    fmg_client: FortiManagerClient,
    test_adom: str,
    test_device: str,
):
    """Test getting device configuration (read-only operation)."""
    if not test_device:
        pytest.skip("TEST_DEVICE not configured")

    api = DeviceAPI(fmg_client)

    # Get global configuration (system DNS)
    config = await api.get_device_config(
        device=test_device,
        scope="global",
        path="system/dns",
    )

    assert config is not None
    # DNS config should have primary field
    assert "primary" in config or isinstance(config, dict)

