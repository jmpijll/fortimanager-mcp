"""Pytest configuration and fixtures for integration tests."""

import asyncio
import logging
import os
from typing import AsyncGenerator

import pytest

from fortimanager_mcp.api.client import FortiManagerClient
from fortimanager_mcp.utils.config import Settings, get_settings

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def settings() -> Settings:
    """Get test settings from environment.

    Raises:
        ValueError: If required settings are missing
    """
    settings = get_settings()

    # Verify FortiManager connection settings
    if not settings.FORTIMANAGER_HOST:
        pytest.skip("FORTIMANAGER_HOST not configured")

    if not settings.has_token_auth and not settings.has_session_auth:
        pytest.skip("No FortiManager authentication configured")

    return settings


@pytest.fixture(scope="session")
async def fmg_client(settings: Settings) -> AsyncGenerator[FortiManagerClient, None]:
    """Provide authenticated FortiManager client for tests.

    This fixture creates a single client for the entire test session
    and cleans up on teardown.

    Yields:
        Authenticated FortiManager client
    """
    logger.info("Connecting to FortiManager for tests")

    client = FortiManagerClient.from_settings(settings)

    try:
        await client.connect()
        logger.info("Successfully connected to FortiManager")
        yield client
    finally:
        logger.info("Disconnecting from FortiManager")
        await client.disconnect()


@pytest.fixture
def test_adom(settings: Settings) -> str:
    """Get ADOM to use for tests.

    Returns:
        ADOM name from TEST_ADOM environment variable or "root"
    """
    return settings.TEST_ADOM


@pytest.fixture
def test_device(settings: Settings) -> str | None:
    """Get device name for device-specific tests.

    Returns:
        Device name from TEST_DEVICE environment variable or None
    """
    return settings.TEST_DEVICE


@pytest.fixture
def skip_write_tests(settings: Settings) -> bool:
    """Check if write tests should be skipped.

    Returns:
        True if write tests should be skipped
    """
    return settings.TEST_SKIP_WRITE_TESTS


@pytest.fixture(autouse=True)
async def cleanup_test_objects(fmg_client: FortiManagerClient, test_adom: str):
    """Ensure test objects are cleaned up after each test.

    This fixture runs automatically after each test to clean up
    any objects with the MCP_TEST_ prefix.
    """
    yield

    # Cleanup logic (runs after test)
    logger.info("Checking for test objects to cleanup")

    try:
        from fortimanager_mcp.api.objects import ObjectAPI

        api = ObjectAPI(fmg_client)

        # List all addresses
        addresses = await api.list_addresses(adom=test_adom)

        # Delete test addresses
        for addr in addresses:
            if addr.name.startswith("MCP_TEST_"):
                logger.info(f"Cleaning up test address: {addr.name}")
                try:
                    await api.delete_address(addr.name, adom=test_adom)
                except Exception as e:
                    logger.warning(f"Failed to cleanup {addr.name}: {e}")

        # List all address groups
        groups = await api.list_address_groups(adom=test_adom)

        # Delete test groups
        for group in groups:
            if group.name.startswith("MCP_TEST_"):
                logger.info(f"Cleaning up test address group: {group.name}")
                try:
                    await api.delete_address_group(group.name, adom=test_adom)
                except Exception as e:
                    logger.warning(f"Failed to cleanup {group.name}: {e}")

    except Exception as e:
        logger.error(f"Error during cleanup: {e}")


# Pytest markers
def pytest_configure(config):
    """Register custom pytest markers."""
    config.addinivalue_line("markers", "readonly: mark test as read-only (safe)")
    config.addinivalue_line("markers", "write: mark test as performing write operations")
    config.addinivalue_line(
        "markers", "device_required: mark test as requiring TEST_DEVICE configuration"
    )

