# Integration Tests for FortiManager MCP Server

## Overview

These integration tests validate the FortiManager MCP server against a real FortiManager instance. Tests are designed to be **non-intrusive** and safe to run against production FortiManager systems.

## Prerequisites

1. **FortiManager Access**
   - FortiManager instance (version 7.2.2+ recommended)
   - Network connectivity to FortiManager
   - Valid credentials (API token or username/password)

2. **Python Environment**
   ```bash
   pip install uv
   uv venv
   source .venv/bin/activate
   uv pip install -e ".[dev]"
   ```

3. **Environment Configuration**
   ```bash
   # Copy and edit .env file
   cp env.example .env
   nano .env
   ```

## Configuration

### Required Environment Variables

```bash
# FortiManager connection
FORTIMANAGER_HOST=192.168.1.99
FORTIMANAGER_API_TOKEN=your-api-token-here

# Or use session-based auth
# FORTIMANAGER_USERNAME=admin
# FORTIMANAGER_PASSWORD=password
```

### Optional Test Configuration

```bash
# ADOM for testing (default: root)
TEST_ADOM=root

# Device name for device-specific tests
TEST_DEVICE=test-device-001

# Skip write operations (run read-only tests only)
TEST_SKIP_WRITE_TESTS=false
```

## Running Tests

### All Tests

```bash
pytest tests/integration/
```

### Read-Only Tests Only

```bash
pytest tests/integration/ -m readonly
```

### Specific Test File

```bash
pytest tests/integration/test_devices.py
```

### With Coverage

```bash
pytest tests/integration/ --cov=src/fortimanager_mcp --cov-report=html
```

### Verbose Output

```bash
pytest tests/integration/ -v
```

### Skip Write Tests

```bash
TEST_SKIP_WRITE_TESTS=true pytest tests/integration/
```

## Test Categories

### Read-Only Tests (Safe)

Marked with `@pytest.mark.readonly`:
- `test_list_devices` - List managed devices
- `test_list_addresses` - List address objects
- `test_list_policies` - List firewall policies
- `test_get_system_status` - Get system status

These tests **do not modify** FortiManager configuration and are completely safe.

### Write Tests (Intrusive)

Marked with `@pytest.mark.write`:
- `test_create_and_delete_address` - Create/delete test address
- `test_create_and_delete_address_group` - Create/delete test group
- `test_create_and_delete_service` - Create/delete test service

These tests:
- Create test objects with `MCP_TEST_` prefix
- Clean up after completion
- Safe for production (objects are temporary and isolated)

### Device-Specific Tests

Marked with `@pytest.mark.device_required`:
- `test_get_device` - Get specific device
- `test_get_device_config` - Get device configuration

These tests require `TEST_DEVICE` environment variable.

## Test Safety

### Non-Intrusive Design

1. **Read-Only Preferred**: Most tests are read-only
2. **Test Object Prefix**: All created objects use `MCP_TEST_` prefix
3. **Automatic Cleanup**: Test objects are deleted after tests
4. **Idempotent**: Tests can run multiple times safely
5. **Isolated**: Test objects don't affect production config

### Cleanup Mechanism

The `cleanup_test_objects` fixture (in `conftest.py`) runs automatically after each test:

```python
@pytest.fixture(autouse=True)
async def cleanup_test_objects(fmg_client, test_adom):
    yield  # Test runs
    # Cleanup all MCP_TEST_* objects
```

### Manual Cleanup

If tests fail and leave test objects:

```python
# List all test objects
from fortimanager_mcp.api.objects import ObjectAPI
api = ObjectAPI(client)
addresses = await api.list_addresses(adom="root")
test_addrs = [a for a in addresses if a.name.startswith("MCP_TEST_")]

# Delete manually
for addr in test_addrs:
    await api.delete_address(addr.name, adom="root")
```

## Troubleshooting

### Connection Failures

```
Error: Connection error: ...
```

**Solutions**:
- Verify `FORTIMANAGER_HOST` is correct
- Check network connectivity: `ping <host>`
- Verify FortiManager is accessible: `curl -k https://<host>/jsonrpc`

### Authentication Failures

```
Error: Authentication failed: ...
```

**Solutions**:
- Verify API token is correct
- Check user has `rpc-permit read-write` configured
- For session auth: verify username/password
- Ensure user is not locked out

### Permission Errors

```
Error: No permission for the resource
```

**Solutions**:
- Verify user has appropriate permissions
- Check user's permission profile
- Verify ADOM access for the user

### Test Skipping

Some tests may be skipped if:
- `TEST_DEVICE` not configured (device-specific tests)
- `TEST_SKIP_WRITE_TESTS=true` (write tests)
- No FortiManager connection configured

### Test Object Cleanup

If cleanup fails:
- Check logs for specific errors
- Verify objects are not in use
- Delete dependencies first (groups before members)

## Test Coverage

Current test coverage:

- ✅ Device Management
  - List devices (read-only)
  - Get device details (read-only)
  - Get device configuration (read-only)
  
- ✅ Firewall Objects
  - List addresses/groups/services (read-only)
  - Create/delete addresses (with cleanup)
  - Create/delete groups (with cleanup)

- 🚧 Policy Management (planned)
  - List packages/policies (read-only)
  - Create/delete policies (with cleanup)

- 🚧 Monitoring (planned)
  - System status (read-only)
  - Task monitoring (read-only)

## Best Practices

1. **Always Run Read-Only First**: Verify connectivity before write tests
2. **Use Test ADOM**: If possible, use dedicated test ADOM
3. **Monitor Logs**: Watch for errors during tests
4. **Verify Cleanup**: Check no test objects remain after tests
5. **Respect Production**: Be cautious with write tests on production systems

## Contributing

When adding new tests:
1. Mark appropriately (`readonly`, `write`, `device_required`)
2. Use `MCP_TEST_` prefix for all created objects
3. Implement cleanup in finally blocks
4. Document test purpose and safety
5. Test against real FortiManager before committing

