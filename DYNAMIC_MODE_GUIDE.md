# Dynamic Tool Loading Mode Guide

## Overview

FortiManager MCP Server now supports **two operational modes** to optimize for different context window sizes:

| Mode | Tools Loaded | Context Usage | Best For |
|------|-------------|---------------|----------|
| **Full** (default) | All 590 tools | ~118K tokens | Large context windows (200K+) |
| **Dynamic** | 5 meta-tools | ~2K tokens | Small context windows (<200K) |

**Key Benefit:** Dynamic mode reduces context consumption by **98%** while maintaining full functionality.

---

## Quick Start

### Enable Dynamic Mode

#### Option 1: Environment Variable
```bash
export FMG_TOOL_MODE=dynamic
python -m fortimanager_mcp
```

#### Option 2: .env File
```bash
# Add to .env
FMG_TOOL_MODE=dynamic
```

#### Option 3: Docker Compose
```yaml
# docker-compose.yml
services:
  fortimanager-mcp:
    environment:
      - FMG_TOOL_MODE=dynamic
      - FORTIMANAGER_HOST=your-host
      - FORTIMANAGER_API_TOKEN=your-token
```

#### Option 4: Claude Desktop
```json
{
  "mcpServers": {
    "fortimanager": {
      "command": "docker",
      "args": [
        "run", "--rm", "-i",
        "-e", "FMG_TOOL_MODE=dynamic",
        "-e", "FORTIMANAGER_HOST=192.168.1.99",
        "-e", "FORTIMANAGER_API_TOKEN=your-token",
        "fortimanager-mcp"
      ]
    }
  }
}
```

---

## How Dynamic Mode Works

### Full Mode (Default Behavior)
```
┌─────────────────┐
│  MCP Server     │
│  590 tools      │  ← All tools loaded at startup
│  ~118K tokens   │
└─────────────────┘
         │
         ▼
   Direct tool call
```

### Dynamic Mode (New)
```
┌─────────────────┐
│  MCP Server     │
│  5 meta-tools   │  ← Only discovery tools loaded
│  ~2K tokens     │
└─────────────────┘
         │
         ▼
  1. Search for tools
  2. Execute by name
  3. Dynamic import & run
```

---

## Meta-Tools Available in Dynamic Mode

### 1. `search_fortimanager_tools`
Find tools by query or category.

**Example:**
```python
search_fortimanager_tools(query="firewall address")
# Returns: List of matching tools with descriptions
```

### 2. `list_fortimanager_categories`
View all tool categories with counts.

**Example:**
```python
list_fortimanager_categories()
# Returns: devices (69), policies (64), objects (47), etc.
```

### 3. `execute_fortimanager_tool`
Run any FortiManager tool by name.

**Example:**
```python
execute_fortimanager_tool(
    tool_name="list_devices",
    adom="root"
)
# Returns: Device list
```

### 4. `get_fortimanager_tool_info`
Get detailed tool documentation.

**Example:**
```python
get_fortimanager_tool_info("create_firewall_address")
# Returns: Parameters, description, usage
```

### 5. `fortimanager_help`
Get help on using dynamic mode.

**Example:**
```python
fortimanager_help()
# Returns: Workflow guide and examples
```

---

## Usage Workflow

### Example 1: List Devices

**In Full Mode:**
```
User: "List all FortiGate devices"
AI:   list_devices(adom="root")
```

**In Dynamic Mode:**
```
User: "List all FortiGate devices"
AI:   Step 1: search_fortimanager_tools(query="list devices")
      → Found: list_devices
      
      Step 2: execute_fortimanager_tool(
          tool_name="list_devices",
          adom="root"
      )
      → Returns device list
```

### Example 2: Create Firewall Address

**In Full Mode:**
```
AI: create_firewall_address(
    name="internal_network",
    subnet="10.0.0.0/8",
    adom="root"
)
```

**In Dynamic Mode:**
```
AI: Step 1: search_fortimanager_tools(
        query="create firewall address",
        category="objects"
    )
    → Found: create_firewall_address
    
    Step 2: get_fortimanager_tool_info("create_firewall_address")
    → Parameters: name, subnet, adom, comment
    
    Step 3: execute_fortimanager_tool(
        tool_name="create_firewall_address",
        name="internal_network",
        subnet="10.0.0.0/8",
        adom="root"
    )
    → Returns success
```

---

## Tool Categories

Dynamic mode organizes 590 tools into 15 categories:

| Category | Count | Description |
|----------|-------|-------------|
| **provisioning** | 98 | CLI templates, system templates, device profiles |
| **devices** | 69 | Device lifecycle, firmware, HA, VDOMs |
| **policies** | 64 | Policy packages, firewall rules, NAT, installation |
| **system** | 47 | Administration, backup, restore, certificates |
| **objects** | 47 | Addresses, services, zones, VIPs, schedules |
| **monitoring** | 43 | System status, device connectivity, tasks |
| **security** | 33 | Web filter, IPS, antivirus, app control, DLP |
| **adom** | 28 | ADOM management, workspace, revisions |
| **vpn** | 24 | IPsec tunnels, SSL-VPN, certificates |
| **fortiguard** | 23 | Updates, contracts, threat feeds |
| **sdwan** | 19 | SD-WAN zones, health checks, services |
| **advanced_objects** | 18 | Dynamic objects, threat feeds, SDN |
| **additional_objects** | 16 | Schedules, internet services, geography |
| **workspace** | 12 | ADOM locking, commits, lock status |
| **scripts** | 12 | CLI script management, execution |

---

## Performance Comparison

### Context Window Usage

| Mode | Tool Definitions | Available for Work | Efficiency |
|------|-----------------|-------------------|------------|
| Full | 118,000 tokens | Context - 118K | Baseline |
| Dynamic | 2,000 tokens | Context - 2K | **98% savings** |

**Example: Claude Sonnet 3.5 (200K context)**
- Full mode: 82K tokens available for work
- Dynamic mode: 198K tokens available for work
- **Gain: 116K tokens (2.4x more working space)**

### Execution Latency

| Mode | First Call | Subsequent Calls |
|------|-----------|------------------|
| Full | <100ms | <100ms |
| Dynamic | <500ms (import) | <100ms (cached) |

**Note:** Python caches imported modules, so dynamic mode overhead is only on first use.

---

## When to Use Each Mode

### Use Full Mode When:
- ✅ You have large context windows (200K+ tokens)
- ✅ You want immediate tool access
- ✅ You're using tools frequently
- ✅ You prefer direct tool calling

### Use Dynamic Mode When:
- ✅ You have limited context windows (<200K tokens)
- ✅ You need more space for complex tasks
- ✅ You're using Claude Desktop or similar
- ✅ You don't mind a discovery step

---

## Troubleshooting

### "Tool not found" Error

**Problem:** Tool name incorrect in `execute_fortimanager_tool()`

**Solution:**
```python
# Use search first to get exact name
search_fortimanager_tools(query="your operation")
# Then use exact name from results
```

### Slow First Execution

**Behavior:** First call to a tool takes ~500ms

**Explanation:** This is normal - Python imports the module on first use. Subsequent calls are fast (~100ms).

### Wrong Mode Active

**Check current mode:**
```bash
# Check health endpoint
curl http://localhost:8000/health

# Or check logs
docker-compose logs fortimanager-mcp | grep "Loading in"
```

**Expected output:**
```
INFO - Loading in DYNAMIC mode - meta-tools only (5 tools)
```

---

## Advanced Usage

### Search Tips

**Broad Search:**
```python
search_fortimanager_tools(query="policy")
# Returns all tools related to policies
```

**Category Filter:**
```python
search_fortimanager_tools(category="devices", limit=50)
# Returns all 69 device tools
```

**Specific Search:**
```python
search_fortimanager_tools(
    query="install",
    category="policies"
)
# Returns policy installation tools only
```

### Chaining Operations

```python
# Step 1: Search
results = search_fortimanager_tools(query="address")

# Step 2: Create address
execute_fortimanager_tool(
    tool_name="create_firewall_address",
    name="dmz_network",
    subnet="172.16.0.0/24",
    adom="root"
)

# Step 3: Verify
execute_fortimanager_tool(
    tool_name="list_firewall_addresses",
    adom="root",
    filter_name="dmz"
)
```

---

## Migration from Full Mode

### No Changes Needed!

Dynamic mode is opt-in. Existing deployments continue working in full mode.

### Gradual Adoption

1. **Test in development:**
   ```bash
   FMG_TOOL_MODE=dynamic docker-compose up
   ```

2. **Monitor performance:**
   - Check logs for mode confirmation
   - Verify tool execution times
   - Test your common workflows

3. **Deploy to production:**
   ```bash
   # Update .env
   FMG_TOOL_MODE=dynamic
   
   # Restart service
   docker-compose restart
   ```

---

## FAQ

### Q: Does dynamic mode have all 590 tools?
**A:** Yes! All tools are available, just loaded on-demand instead of at startup.

### Q: Is dynamic mode slower?
**A:** Slightly (~500ms first call, then cached). The context savings usually outweigh this.

### Q: Can I switch modes without redeploying?
**A:** Yes, just restart the container with different `FMG_TOOL_MODE` value.

### Q: Which mode should I use?
**A:** 
- Large context (200K+): Full mode
- Small context (<200K): Dynamic mode
- Not sure: Try dynamic mode first

### Q: Are there any missing features in dynamic mode?
**A:** No! All features work identically. Only the loading mechanism differs.

---

## Technical Details

See [ADR-006: Dynamic Tool Loading](.notes/decisions/ADR-006-dynamic-tool-loading.md) for:
- Architecture decisions
- Implementation details
- Performance implications
- Testing strategy
- Future enhancements

---

## Support

**Issues:** [GitHub Issues](https://github.com/jmpijll/fortimanager-mcp/issues)
**Documentation:** [.notes Directory](.notes/)
**ADR:** [ADR-006](.notes/decisions/ADR-006-dynamic-tool-loading.md)

---

*FortiManager MCP Server - Optimized for any context window size*

