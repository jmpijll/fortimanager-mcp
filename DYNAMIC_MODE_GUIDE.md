# Dynamic Tool Loading Mode Guide (v2)

## Overview

FortiManager MCP Server supports **two operational modes** optimized for different context window sizes:

| Mode | Tools Loaded | Context Usage | Best For |
|------|-------------|---------------|----------|
| **Full** (default) | All 590 tools | ~118K tokens | Large contexts (200K+) |
| **Dynamic** | ~15 direct tools | ~3-4K tokens | Small contexts (<200K) |

**Key Benefits:**
- ✅ **96-97% context reduction** (118K → 3-4K tokens)
- ✅ **Natural LLM interface** - Direct tool calls like `list_adoms()`
- ✅ **Full functionality** - All 590 operations accessible
- ✅ **Better usability** - No confusing 2-step workflows

---

## Quick Start

### Enable Dynamic Mode

```bash
# Option 1: Environment variable
export FMG_TOOL_MODE=dynamic

# Option 2: .env file
echo "FMG_TOOL_MODE=dynamic" >> .env

# Option 3: Docker Compose
docker-compose up  # Uses FMG_TOOL_MODE from environment
```

---

## How It Works

### The Problem with Meta-Tools

**Initial Approach (v1) - ❌ Didn't Work:**
```
LLM sees: search_fortimanager_tools(), execute_fortimanager_tool()
User asks: "List all ADOMs"
LLM tries: search... then execute... (FAILS - too indirect)
```

**Why it failed:**
- LLMs struggled with 2-step workflows
- `execute_fortimanager_tool(tool_name="...")` was too generic
- Indirect pattern was unintuitive

### The Solution: Direct Proxy Tools

**Current Approach (v2) - ✅ Works Great:**
```
LLM sees: list_adoms(), list_devices(), create_firewall_address()
User asks: "List all ADOMs"
LLM calls: list_adoms() → SUCCESS!
```

**Why it works:**
- Direct, action-oriented tool names
- Natural interface matching user intent
- LLMs understand "list_adoms" immediately
- No meta-cognition required

---

## Available Tools in Dynamic Mode

### Core Direct Tools (~15 tools)

#### ADOM Management
```python
list_adoms()
# Lists all Administrative Domains

get_adom_details(adom="root")
# Gets detailed ADOM information
```

#### Device Management
```python
list_devices(adom=None)
# Lists all managed FortiGate devices

get_device_details(name="FGT-001", adom=None)
# Gets detailed device information
```

#### Firewall Objects
```python
list_firewall_addresses(adom="root", filter_name=None)
# Lists firewall address objects

create_firewall_address(name="internal", subnet="10.0.0.0/8", adom="root", comment=None)
# Creates a new firewall address
```

#### Policy Management
```python
list_policy_packages(adom="root")
# Lists all policy packages

list_firewall_policies(adom="root", package="default")
# Lists firewall policies in a package
```

#### System Monitoring
```python
get_system_status()
# Gets FortiManager system status

list_tasks(limit=None)
# Lists recent system tasks
```

### Discovery Tools (for advanced operations)

For less common operations (VPN, SD-WAN, advanced configs):

```python
find_fortimanager_tool(operation="create VPN tunnel")
# Searches all 590 operations, returns matches with usage instructions

execute_advanced_tool(tool_name="create_vpn_ipsec_phase1", name="my_vpn", ...)
# Executes any of the 590 operations

list_fortimanager_categories()
# Shows all 15 categories with tool counts
```

---

## Usage Examples

### Example 1: Common Operation (Direct Call)

**User Request:** "Show me all ADOMs"

**LLM Response:**
```python
list_adoms()
```

**Result:** ✅ Works immediately - natural, direct call

---

### Example 2: Device Listing (With Filter)

**User Request:** "List devices in the production ADOM"

**LLM Response:**
```python
list_devices(adom="production")
```

**Result:** ✅ Simple parameter, clear intent

---

### Example 3: Create Firewall Object

**User Request:** "Create a firewall address for the DMZ network 172.16.0.0/24"

**LLM Response:**
```python
create_firewall_address(
    name="dmz_network",
    subnet="172.16.0.0/24",
    adom="root",
    comment="DMZ network range"
)
```

**Result:** ✅ Natural, matches user's intent

---

### Example 4: Advanced Operation (VPN Tunnel)

**User Request:** "Set up an IPsec VPN tunnel to 1.2.3.4"

**LLM Response:**
```python
# Step 1: Find the right tool
find_fortimanager_tool(operation="create VPN tunnel")

# Step 2: Use the found tool
execute_advanced_tool(
    tool_name="create_vpn_ipsec_phase1",
    name="branch_vpn",
    remote_gw="1.2.3.4",
    adom="root",
    ...
)
```

**Result:** ✅ Discovery pattern works for complex operations

---

## Comparison: Full vs Dynamic Mode

### Tool Availability

| Aspect | Full Mode | Dynamic Mode |
|--------|-----------|--------------|
| **Common operations** | Direct tools | Direct tools (same!) |
| **Advanced operations** | Direct tools | Via find + execute |
| **Context usage** | ~118K tokens | ~3-4K tokens |
| **LLM experience** | Natural | Natural for common, 2-step for advanced |

### Example Workflows

**Listing ADOMs:**
- **Full mode:** `list_adoms()` 
- **Dynamic mode:** `list_adoms()` ← **Same experience!**

**Creating VPN:**
- **Full mode:** `create_vpn_ipsec_phase1(...)`
- **Dynamic mode:** `find_fortimanager_tool()` → `execute_advanced_tool()`

---

## Performance

### Context Window Impact

**Claude Sonnet 3.5 (200K context):**
- **Full mode:** 82K tokens available for work
- **Dynamic mode:** 196K tokens available for work
- **Gain:** +114K tokens (2.4x more space)

### Execution Speed

| Operation Type | Full Mode | Dynamic Mode |
|---------------|-----------|--------------|
| Common (direct tools) | <100ms | <100ms |
| Advanced (first call) | <100ms | <500ms (import) |
| Advanced (cached) | <100ms | <100ms |

---

## Architecture

### How Proxy Tools Work

```python
# What the LLM sees and calls:
list_adoms()

# What happens internally:
@mcp.tool()
async def list_adoms() -> dict:
    """List all Administrative Domains."""
    return await execute_tool_dynamic("list_adoms")

# execute_tool_dynamic():
# 1. Gets tool metadata from registry
# 2. Dynamically imports the module
# 3. Calls the actual implementation
# 4. Returns result
```

**Benefits:**
- LLM sees natural tool names
- Internal implementation stays clean
- Dynamic loading saves context
- Full functionality preserved

---

## Tool Selection Strategy

### Which Operations Get Direct Tools?

**Criteria for direct tools:**
1. ✅ Used frequently (ADOMs, devices, policies)
2. ✅ Simple, clear action (list, get, create)
3. ✅ Match common user requests
4. ✅ <20% of operations (to stay under ~4K tokens)

**Current direct tools (~15):**
- ADOM: list, get details
- Devices: list, get details
- Addresses: list, create
- Policies: list packages, list policies
- System: status, tasks

**All other operations (575):**
- Available via `find_fortimanager_tool()` + `execute_advanced_tool()`
- Full documentation, parameters, examples provided
- Same functionality, just 2-step access

---

## When to Use Each Mode

### Use Full Mode When:
- ✅ Large context windows (200K+ tokens)
- ✅ Need ALL tools immediately visible
- ✅ Building automation/scripts
- ✅ Working with many advanced operations

### Use Dynamic Mode When:
- ✅ Limited context (<200K tokens)
- ✅ Primarily using common operations
- ✅ Using Claude Desktop or similar
- ✅ Need context space for complex tasks

---

## Troubleshooting

### Issue: "Tool not found"

**Problem:** LLM tries to call a tool that doesn't have a direct proxy

**Solution:** Use discovery pattern:
```python
find_fortimanager_tool(operation="what you want to do")
execute_advanced_tool(tool_name="...", ...)
```

### Issue: LLM not using tools

**Problem:** Tool descriptions unclear

**Solution:** Each direct tool has clear examples:
```python
list_adoms()
# Example: "Show me all ADOMs" → list_adoms()
```

### Issue: Slow first advanced call

**Behavior:** First call to advanced operation takes ~500ms

**Explanation:** Dynamic import overhead. Subsequent calls are fast (<100ms).

---

## Migration Guide

### From Full Mode

**No changes needed!** Just set `FMG_TOOL_MODE=dynamic` and restart.

Common operations work identically:
```python
# Works in both modes:
list_adoms()
list_devices()
create_firewall_address(...)
```

### From Dynamic Mode v1 (Meta-Tools)

**Old approach (meta-tools):**
```python
search_fortimanager_tools(query="list adoms")
execute_fortimanager_tool(tool_name="list_adoms")
```

**New approach (direct tools):**
```python
list_adoms()  # Just call it directly!
```

---

## Technical Details

### Files Changed
- `src/fortimanager_mcp/tools/proxy_tools.py` - Direct proxy tool implementations
- `src/fortimanager_mcp/server.py` - Loads proxy_tools in dynamic mode
- `src/fortimanager_mcp/utils/tool_registry.py` - Tool metadata and execution

### Tool Count
- **Full mode:** 590 tools loaded
- **Dynamic mode:** ~15 direct + 2 discovery tools loaded
- **Accessible:** All 590 operations in both modes

### Context Calculation
```
Full mode:
  590 tools × ~200 tokens each = ~118,000 tokens

Dynamic mode:
  15 direct tools × ~200 tokens = ~3,000 tokens
  2 discovery tools × ~300 tokens = ~600 tokens
  Total: ~3,600 tokens
  
Savings: 97% reduction
```

---

## FAQ

**Q: Do I lose functionality in dynamic mode?**
A: No! All 590 operations accessible. Common ones are direct, advanced use find+execute.

**Q: Why not just load all 590 tools?**
A: Context window space. Dynamic mode gives you 114K more tokens for your actual task.

**Q: Is dynamic mode slower?**
A: Common operations: same speed. Advanced operations: ~500ms first call, then cached.

**Q: Can I add more direct tools?**
A: Yes! Edit `proxy_tools.py` to add tools you use frequently.

**Q: How does LLM know which tool to use?**
A: Direct tools have clear names and examples. LLMs understand `list_adoms()` naturally.

---

## Support

**Issues:** [GitHub Issues](https://github.com/jmpijll/fortimanager-mcp/issues)
**Branch:** `feature/dynamic-tool-loading`
**Documentation:** [ADR-006](.notes/decisions/ADR-006-dynamic-tool-loading.md)

---

*FortiManager MCP Server - Optimized for any context window, natural for any LLM*

