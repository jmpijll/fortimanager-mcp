# ADR-004: Integration Testing Strategy

## Status
Accepted

## Context
We need a testing strategy that validates the MCP server and FortiManager API client without being intrusive to production FortiManager environments. The user has explicitly stated a preference for integration tests against a real FortiManager instance.

## Decision
Implement **integration tests only** against a real FortiManager instance, with a focus on **non-intrusive operations**.

## Rationale

### No Unit Tests with Mocks

#### Why Skip Unit Tests?
1. **Real API Validation**: Integration tests validate actual FortiManager API behavior
2. **Mock Limitations**: Mocks can't catch real API changes or edge cases
3. **Development Speed**: Less time maintaining mock fixtures
4. **User Preference**: User explicitly requested integration tests against real instance

#### What We Lose
- Faster test execution
- Ability to test without FortiManager access
- Isolation from external dependencies

#### What We Gain
- Confidence in real-world functionality
- Detection of API changes
- Validation of actual FortiManager responses
- No mock maintenance burden

### Non-Intrusive Testing Principles

#### Read-Only Operations (Preferred)
- List devices
- Get device details
- List ADOMs
- Get ADOM details
- List firewall objects
- Get policy details
- Check system status
- View task history

These operations don't modify FortiManager state and are completely safe.

#### Test Object Operations (When Write Tests Needed)
When testing create/update/delete operations:
1. **Naming Convention**: All test objects use `MCP_TEST_` prefix
2. **Immediate Cleanup**: Delete test objects after test completion
3. **Idempotent Tests**: Tests can run multiple times safely
4. **Isolated Objects**: Test objects don't interact with production config

Example:
```python
async def test_create_address():
    # Create test object
    address = await client.create_address(
        adom="root",
        name="MCP_TEST_address_001",
        subnet="10.255.255.1/32"
    )
    
    try:
        # Verify creation
        assert address["name"] == "MCP_TEST_address_001"
    finally:
        # Always cleanup
        await client.delete_address(adom="root", name="MCP_TEST_address_001")
```

#### Operations to Avoid
- Installing configurations to devices
- Modifying existing production objects
- Changing system settings
- Operations affecting device connectivity
- Policy package installations

### Test Environment Configuration

#### Environment Variables
```bash
# Required for all tests
FORTIMANAGER_HOST=192.168.1.99
FORTIMANAGER_API_TOKEN=test-token

# Optional test configuration
TEST_ADOM=root                    # ADOM to use for tests
TEST_DEVICE=test-device-001       # Device for device-specific tests
TEST_SKIP_WRITE_TESTS=false       # Skip write operations if true
```

#### Test Fixtures
```python
@pytest.fixture
async def fmg_client():
    """Provide authenticated FortiManager client."""
    settings = Settings()
    client = FortiManagerClient(
        host=settings.FORTIMANAGER_HOST,
        api_token=settings.FORTIMANAGER_API_TOKEN,
        verify_ssl=settings.FORTIMANAGER_VERIFY_SSL
    )
    yield client
    # Cleanup happens in individual tests
```

## Test Organization

### Test Categories

#### 1. API Client Tests (`tests/integration/`)

**test_devices.py** - Device Management
- ✅ `test_list_devices()` - Read-only
- ✅ `test_get_device_details()` - Read-only
- ✅ `test_get_device_status()` - Read-only
- ⚠️ `test_add_device()` - Creates test device, then deletes
- ⚠️ `test_update_device()` - Uses test device
- ⚠️ `test_delete_device()` - Cleanup test device

**test_adoms.py** - ADOM Management
- ✅ `test_list_adoms()` - Read-only
- ✅ `test_get_adom_details()` - Read-only

**test_objects.py** - Firewall Objects
- ✅ `test_list_addresses()` - Read-only
- ⚠️ `test_create_address()` - Creates `MCP_TEST_*`, then deletes
- ⚠️ `test_update_address()` - Uses test address
- ⚠️ `test_delete_address()` - Cleanup test address
- ✅ `test_list_address_groups()` - Read-only
- Similar patterns for services, schedules, etc.

**test_policies.py** - Policy Management
- ✅ `test_list_policy_packages()` - Read-only
- ✅ `test_list_policies()` - Read-only
- ✅ `test_get_policy_details()` - Read-only
- ⚠️ Skip policy creation tests (too complex, affects security)

**test_monitoring.py** - Monitoring
- ✅ `test_get_system_status()` - Read-only
- ✅ `test_list_tasks()` - Read-only
- ✅ `test_get_task_status()` - Read-only (use existing task)

#### 2. MCP Tools Tests (`tests/integration/test_tools.py`)
Test the MCP tools end-to-end:
- Tool registration
- Input validation
- Output formatting
- Error handling

### Test Execution

```bash
# Run all tests
pytest tests/integration/

# Run only read-only tests
pytest tests/integration/ -m "readonly"

# Skip write tests
TEST_SKIP_WRITE_TESTS=true pytest tests/integration/

# Run specific test category
pytest tests/integration/test_devices.py
```

### Test Markers
```python
# Mark read-only tests
@pytest.mark.readonly
async def test_list_devices(fmg_client):
    ...

# Mark write tests
@pytest.mark.write
async def test_create_address(fmg_client):
    ...
```

## Consequences

### Positive
- Real-world validation of API integration
- Confidence in production behavior
- Catch actual FortiManager API changes
- No mock maintenance overhead
- Faster development (no mock setup)

### Negative
- Requires FortiManager instance for testing
- Slower test execution (network I/O)
- Tests can fail due to network issues
- Need credentials management
- Can't run in CI without FortiManager access

### Mitigation Strategies

#### For Slower Tests
- Run tests on-demand, not on every commit
- Use test markers to run subsets
- Parallel test execution where safe

#### For FortiManager Dependency
- Document setup requirements
- Provide test FortiManager VM configuration
- Consider mock mode for CI in future

#### For Credentials
- Never commit credentials
- Use environment variables
- Document credential generation process

## Safety Measures

### Test Isolation
```python
@pytest.fixture(autouse=True)
async def cleanup_test_objects(fmg_client):
    """Ensure no test objects remain after tests."""
    yield
    # Cleanup any objects with MCP_TEST_ prefix
    await cleanup_mcp_test_objects(fmg_client)
```

### Failure Handling
```python
try:
    # Test operation
    await test_operation()
finally:
    # Always cleanup, even on test failure
    await cleanup()
```

### Test Data Validation
- Use unique IDs/names for test objects
- Verify test object doesn't exist before creation
- Confirm deletion after cleanup

## Documentation Requirements

### Test README
Create `tests/integration/README.md`:
- Setup instructions
- Credential configuration
- FortiManager requirements
- How to run tests
- Troubleshooting guide

### Test Object Tracking
Log all test object creation:
```python
logger.info(f"Created test object: {name} (cleanup required)")
```

## Future Enhancements
- Add mock mode for CI/CD pipelines
- Implement test FortiManager simulator
- Add performance benchmarks
- Create test data generator

## References
- pytest-asyncio documentation
- FortiManager API documentation
- Integration testing best practices

