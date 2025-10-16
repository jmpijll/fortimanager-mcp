# ADR-005: Tool Categorization by FortiManager API Domains

## Status
Accepted

## Context
FortiManager provides a comprehensive JSON RPC API covering many functional areas. We need to organize MCP tools in a logical way that:
1. Makes tools discoverable for AI assistants
2. Aligns with FortiManager's API structure
3. Keeps code maintainable and organized
4. Follows single-responsibility principle

## Decision
Organize MCP tools into **domain-specific modules** matching FortiManager API functional areas, with each tool having a **single, clear purpose**.

## Tool Categories

### 1. Device Management Tools (`tools/device_tools.py`)

Maps to FortiManager Device Manager functionality.

**Tools**:
- `list_devices` - List all managed devices
- `get_device` - Get specific device details
- `add_device` - Add new managed device
- `remove_device` - Remove managed device
- `update_device_settings` - Update device configuration
- `install_device_settings` - Push pending device settings

**API Endpoints**:
- `/dvmdb/device`
- `/pm/config/device/{device}/global/*`
- `/pm/config/device/{device}/vdom/{vdom}/*`
- `/securityconsole/install/device`

### 2. ADOM Management Tools (`tools/adom_tools.py`)

Administrative Domain operations.

**Tools**:
- `list_adoms` - List all ADOMs
- `get_adom` - Get ADOM details
- `create_adom` - Create new ADOM
- `delete_adom` - Delete ADOM
- `lock_adom` - Lock ADOM for editing
- `unlock_adom` - Unlock ADOM

**API Endpoints**:
- `/dvmdb/adom`

### 3. Firewall Object Tools (`tools/object_tools.py`)

Security object management in ADOMs.

**Tools**:
- `list_firewall_addresses` - List firewall address objects
- `create_firewall_address` - Create address object
- `update_firewall_address` - Update address object
- `delete_firewall_address` - Delete address object
- `list_address_groups` - List address groups
- `create_address_group` - Create address group
- `update_address_group` - Update address group
- `delete_address_group` - Delete address group
- `list_services` - List service objects
- `create_service` - Create service object
- `update_service` - Update service object
- `delete_service` - Delete service object
- `list_service_groups` - List service groups
- Similar tools for schedules, VIPs, IP pools, etc.

**API Endpoints**:
- `/pm/config/adom/{adom}/obj/firewall/address`
- `/pm/config/adom/{adom}/obj/firewall/addrgrp`
- `/pm/config/adom/{adom}/obj/firewall/service/custom`
- `/pm/config/adom/{adom}/obj/firewall/service/group`
- `/pm/config/adom/{adom}/obj/firewall/schedule/recurring`
- `/pm/config/adom/{adom}/obj/firewall/vip`
- etc.

### 4. Policy Management Tools (`tools/policy_tools.py`)

Firewall policy and policy package operations.

**Tools**:
- `list_policy_packages` - List policy packages in ADOM
- `get_policy_package` - Get package details
- `create_policy_package` - Create new policy package
- `delete_policy_package` - Delete policy package
- `list_firewall_policies` - List policies in package
- `get_firewall_policy` - Get specific policy
- `create_firewall_policy` - Create firewall policy
- `update_firewall_policy` - Update firewall policy
- `delete_firewall_policy` - Delete firewall policy
- `move_firewall_policy` - Reorder policies
- `install_policy_package` - Install security settings

**API Endpoints**:
- `/pm/config/adom/{adom}/pkg`
- `/pm/config/adom/{adom}/pkg/{pkg}/firewall/policy`
- `/securityconsole/install/package`

### 5. Monitoring Tools (`tools/monitoring_tools.py`)

System monitoring and task tracking.

**Tools**:
- `get_system_status` - Get FortiManager status
- `get_device_status` - Check device connectivity
- `list_tasks` - List recent tasks
- `get_task_status` - Monitor specific task
- `get_task_history` - Get task execution history
- `check_pending_changes` - List pending changes

**API Endpoints**:
- `/cli/global/system/status`
- `/task/task`
- `/task/task/{id}`
- `/dvmdb/device` (with status fields)

### 6. VPN Management Tools (`tools/vpn_tools.py`) - Future

IPsec VPN configuration (Phase 2 implementation).

**Tools**: TBD based on FortiManager VPN API
- VPN Phase 1/Phase 2 interfaces
- VPN tunnels
- Dynamic VPN

### 7. SD-WAN Tools (`tools/sdwan_tools.py`) - Future

SD-WAN configuration (Phase 2 implementation).

**Tools**: TBD based on FortiManager SD-WAN API

## Tool Design Principles

### Single Responsibility
Each tool does **one thing well**:
```python
# Good: Focused tool
@mcp.tool()
def list_firewall_addresses(adom: str) -> list[dict]:
    """List all firewall address objects in an ADOM."""
    ...

# Bad: Tool doing too much
@mcp.tool()
def manage_firewall_addresses(action: str, adom: str, ...):
    """Create, update, delete, or list addresses."""
    ...
```

### Clear Naming
Tool names follow patterns:
- `list_*` - Get multiple items
- `get_*` - Get single item details
- `create_*` - Create new item
- `update_*` - Modify existing item
- `delete_*` / `remove_*` - Delete item
- `install_*` - Push configuration
- `check_*` - Status check

### Rich Descriptions
Every tool has a comprehensive docstring:
```python
@mcp.tool()
def create_firewall_address(
    adom: str,
    name: str,
    subnet: str,
    comment: str = ""
) -> dict:
    """Create a new firewall address object in FortiManager.
    
    Creates a subnet-type firewall address object that can be used in
    firewall policies and other security configurations.
    
    Args:
        adom: Administrative Domain name (e.g., 'root')
        name: Unique name for the address object
        subnet: IP address and netmask in CIDR format (e.g., '192.168.1.0/24')
        comment: Optional description for the address object
    
    Returns:
        Dictionary containing the created address object details
    
    Raises:
        FortiManagerError: If creation fails (duplicate name, invalid subnet, etc.)
    
    Example:
        create_firewall_address(
            adom="root",
            name="internal_network",
            subnet="10.0.0.0/8",
            comment="RFC1918 internal network"
        )
    """
    ...
```

### Input Validation
Use Pydantic models for validation:
```python
from pydantic import BaseModel, Field, validator

class CreateAddressInput(BaseModel):
    adom: str = Field(..., description="ADOM name")
    name: str = Field(..., min_length=1, max_length=63)
    subnet: str = Field(..., pattern=r"^\d+\.\d+\.\d+\.\d+/\d+$")
    comment: str = Field("", max_length=255)
    
    @validator("subnet")
    def validate_subnet(cls, v):
        # Additional validation logic
        return v
```

### Structured Output
Return consistent, structured responses:
```python
{
    "status": "success",
    "data": {
        "name": "internal_network",
        "subnet": "10.0.0.0/8",
        "uuid": "..."
    },
    "message": "Address created successfully"
}
```

## File Organization

```
src/fortimanager_mcp/tools/
├── __init__.py              # Export all tools
├── device_tools.py          # ~10-15 device tools
├── adom_tools.py            # ~6-8 ADOM tools
├── object_tools.py          # ~30-40 object tools (largest)
├── policy_tools.py          # ~15-20 policy tools
└── monitoring_tools.py      # ~8-10 monitoring tools
```

Each file:
- Imports from `fortimanager_mcp.api.*`
- Defines tools using `@mcp.tool()` decorator
- Includes comprehensive docstrings
- Handles errors appropriately

## Registration Pattern

```python
# In server.py
from mcp.server.fastmcp import FastMCP
from fortimanager_mcp.utils.config import settings
from fortimanager_mcp.api.client import FortiManagerClient

# Create MCP server
mcp = FastMCP("FortiManager API Server", stateless_http=True)

# Initialize API client
fmg_client = FortiManagerClient(
    host=settings.FORTIMANAGER_HOST,
    api_token=settings.FORTIMANAGER_API_TOKEN
)

# Import tools (automatically registers via decorators)
from fortimanager_mcp.tools import device_tools
from fortimanager_mcp.tools import adom_tools
from fortimanager_mcp.tools import object_tools
from fortimanager_mcp.tools import policy_tools
from fortimanager_mcp.tools import monitoring_tools
```

## Consequences

### Positive
- Clear organization matching FortiManager structure
- Easy to find and add new tools
- Single-responsibility makes tools easier to understand
- AI assistants can discover relevant tools by category
- Code reuse through shared API client
- Testing organized by domain

### Negative
- Many small functions (potential for code duplication)
- Need to maintain consistency across tools
- Large number of tools (~100+ eventually)

### Mitigation
- Shared utilities for common patterns
- Consistent naming and structure
- Code generation templates for new tools
- Comprehensive tool registry documentation

## Tool Discovery for AI

When an AI assistant lists tools, they'll see:

```
Device Management:
- list_devices: List all managed FortiGate devices
- get_device: Get detailed information about a specific device
- add_device: Add a new FortiGate device to FortiManager
- ...

Firewall Objects:
- list_firewall_addresses: List all firewall address objects
- create_firewall_address: Create a new firewall address object
- update_firewall_address: Update an existing address object
- ...

Policies:
- list_firewall_policies: List firewall policies in a package
- create_firewall_policy: Create a new firewall policy rule
- install_policy_package: Push policy changes to devices
- ...
```

## References
- FortiManager JSON API Reference
- FortiManager-how-to-guide documentation
- MCP Tool Best Practices
- Single Responsibility Principle

