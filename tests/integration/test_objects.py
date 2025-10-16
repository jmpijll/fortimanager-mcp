"""Integration tests for firewall object management API."""

import pytest

from fortimanager_mcp.api.client import FortiManagerClient
from fortimanager_mcp.api.objects import ObjectAPI


@pytest.mark.readonly
@pytest.mark.asyncio
async def test_list_addresses(fmg_client: FortiManagerClient, test_adom: str):
    """Test listing firewall addresses (read-only operation)."""
    api = ObjectAPI(fmg_client)
    addresses = await api.list_addresses(adom=test_adom)

    assert isinstance(addresses, list)
    # Addresses list may be empty in new ADOM
    if addresses:
        addr = addresses[0]
        assert addr.name
        assert hasattr(addr, "type")


@pytest.mark.readonly
@pytest.mark.asyncio
async def test_list_address_groups(fmg_client: FortiManagerClient, test_adom: str):
    """Test listing address groups (read-only operation)."""
    api = ObjectAPI(fmg_client)
    groups = await api.list_address_groups(adom=test_adom)

    assert isinstance(groups, list)
    if groups:
        group = groups[0]
        assert group.name
        assert hasattr(group, "member")


@pytest.mark.readonly
@pytest.mark.asyncio
async def test_list_services(fmg_client: FortiManagerClient, test_adom: str):
    """Test listing firewall services (read-only operation)."""
    api = ObjectAPI(fmg_client)
    services = await api.list_services(adom=test_adom)

    assert isinstance(services, list)
    if services:
        svc = services[0]
        assert svc.name
        assert hasattr(svc, "protocol")


@pytest.mark.write
@pytest.mark.asyncio
async def test_create_and_delete_address(
    fmg_client: FortiManagerClient,
    test_adom: str,
    skip_write_tests: bool,
):
    """Test creating and deleting a firewall address."""
    if skip_write_tests:
        pytest.skip("Write tests skipped")

    api = ObjectAPI(fmg_client)

    # Create test address
    test_name = "MCP_TEST_address_001"
    test_subnet = "10.255.255.1/32"

    address = await api.create_address(
        name=test_name,
        subnet=test_subnet,
        adom=test_adom,
        comment="Test address created by integration test",
    )

    try:
        assert address.name == test_name
        assert address.type in ("ipmask", 0)  # Can be symbolic or numeric

        # Verify it was created by retrieving it
        retrieved = await api.get_address(name=test_name, adom=test_adom)
        assert retrieved.name == test_name

    finally:
        # Always cleanup
        await api.delete_address(name=test_name, adom=test_adom)


@pytest.mark.write
@pytest.mark.asyncio
async def test_create_and_delete_address_group(
    fmg_client: FortiManagerClient,
    test_adom: str,
    skip_write_tests: bool,
):
    """Test creating and deleting an address group."""
    if skip_write_tests:
        pytest.skip("Write tests skipped")

    api = ObjectAPI(fmg_client)

    # First create member addresses
    member1_name = "MCP_TEST_member_001"
    member2_name = "MCP_TEST_member_002"
    group_name = "MCP_TEST_group_001"

    try:
        # Create member addresses
        await api.create_address(name=member1_name, subnet="10.1.1.1/32", adom=test_adom)
        await api.create_address(name=member2_name, subnet="10.1.1.2/32", adom=test_adom)

        # Create group
        group = await api.create_address_group(
            name=group_name,
            members=[member1_name, member2_name],
            adom=test_adom,
            comment="Test group created by integration test",
        )

        assert group.name == group_name
        assert len(group.member) == 2

    finally:
        # Cleanup: delete group first, then members
        try:
            await api.delete_address_group(name=group_name, adom=test_adom)
        except:
            pass

        try:
            await api.delete_address(name=member1_name, adom=test_adom)
        except:
            pass

        try:
            await api.delete_address(name=member2_name, adom=test_adom)
        except:
            pass

