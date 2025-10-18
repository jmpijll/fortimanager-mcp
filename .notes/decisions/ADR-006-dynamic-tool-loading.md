# ADR-006: Dynamic Tool Loading for Context Window Optimization

## Status
Accepted

## Context

The FortiManager MCP server implements 590 tools covering 100% of the FortiManager 7.4.8 API. While this provides complete functionality, it presents challenges for AI assistants with smaller context windows:

**Problem:**
- 590 tool definitions consume ~118,000 tokens just for tool metadata
- Smaller context windows (e.g., Claude Sonnet 3.5 ~200K tokens) have limited space for actual work
- Users with large contexts don't have this problem and benefit from having all tools visible
- Need a solution that works for both small and large context scenarios

**Requirements:**
1. Maintain full 590-tool functionality
2. Support both small and large context windows
3. Single MCP server deployment
4. Easy to configure and use
5. No breaking changes to existing users

## Decision

Implement **dual-mode operation** with environment variable switching:
- **Full Mode** (default): Load all 590 tools at startup (current behavior)
- **Dynamic Mode**: Load only meta-tools, execute tools on-demand

### Architecture

#### Full Mode (`FMG_TOOL_MODE=full`)
```
Startup: Import all 26 tool modules → 590 tools registered
Context: ~118K tokens for tool definitions
Usage: Normal MCP tool calling (current behavior)
```

#### Dynamic Mode (`FMG_TOOL_MODE=dynamic`)
```
Startup: Import meta_tools module only → 5 tools registered
Context: ~2K tokens for meta-tool definitions (98% reduction)
Usage: 3-step workflow:
  1. search_fortimanager_tools(query="...")
  2. get_fortimanager_tool_info(tool_name="...")  
  3. execute_fortimanager_tool(tool_name="...", **params)
```

### Key Components

#### 1. Tool Registry (`utils/tool_registry.py`)
- Maintains metadata for all 590 tools
- Provides search and discovery functions
- Enables dynamic tool execution without loading modules

#### 2. Meta-Tools (`tools/meta_tools.py`)
Five discovery and execution tools:
- `search_fortimanager_tools()` - Find tools by query/category
- `list_fortimanager_categories()` - Show all categories
- `get_fortimanager_tool_info()` - Get detailed tool docs
- `execute_fortimanager_tool()` - Execute any tool by name
- `fortimanager_help()` - Usage guide for dynamic mode

#### 3. Configuration (`utils/config.py`)
- `FMG_TOOL_MODE` setting (full|dynamic, default: full)
- Environment variable: `FMG_TOOL_MODE=dynamic`

#### 4. Conditional Loading (`server.py`)
```python
if settings.FMG_TOOL_MODE == "dynamic":
    # Load only meta-tools
    from fortimanager_mcp.tools import meta_tools
else:
    # Load all 26 tool modules (590 tools)
    from fortimanager_mcp.tools import device_tools, object_tools, ...
```

## Implementation Details

### Dynamic Tool Execution

Tools are executed through dynamic import:

```python
async def execute_tool_dynamic(tool_name: str, **kwargs: Any) -> Any:
    # Get tool metadata from registry
    metadata = get_tool_metadata(tool_name)
    
    # Dynamically import module
    module = importlib.import_module(metadata.module)
    
    # Get and execute function
    tool_func = getattr(module, tool_name)
    result = await tool_func(**kwargs)
    
    return result
```

### Tool Registry Structure

```python
TOOL_REGISTRY = {
    "list_devices": ToolMetadata(
        name="list_devices",
        module="fortimanager_mcp.tools.device_tools",
        category="devices",
        description="List all managed FortiGate devices",
        parameters={"adom": {"type": "string", "optional": True}},
    ),
    # ... 589 more tools
}
```

### Usage Workflow in Dynamic Mode

**Step 1: Discovery**
```
User: "List all FortiGate devices"
AI: search_fortimanager_tools(query="list devices")
Result: Found "list_devices" tool
```

**Step 2: Execution**
```
AI: execute_fortimanager_tool(
    tool_name="list_devices",
    adom="root"
)
Result: Device list returned
```

## Alternatives Considered

### Alternative 1: Multiple Specialized Servers
**Approach:** Split into 5 separate servers (devices, security, objects, etc.)

**Pros:**
- Clear separation by domain
- Each server ~100-150 tools

**Cons:**
- ❌ Multiple deployments/Docker images
- ❌ Users must choose right server
- ❌ Operations may span servers
- ❌ Against user requirement for single server

**Decision:** Rejected - User prefers single server

### Alternative 2: Tool Consolidation
**Approach:** Merge similar tools with operation parameters

**Pros:**
- Fewer tools (~50-100 instead of 590)

**Cons:**
- ❌ Violates ADR-005 single responsibility
- ❌ Less discoverable for LLMs
- ❌ Complex tool signatures
- ❌ Major refactoring required

**Decision:** Rejected - Violates project principles

### Alternative 3: Hierarchical Proxy Pattern
**Approach:** Single proxy tool routes to all operations

**Pros:**
- Minimal context usage

**Cons:**
- ❌ Complex semantic matching
- ❌ Less structured interface
- ❌ LLMs may struggle
- ❌ High implementation complexity

**Decision:** Rejected - Too complex, less reliable

## Consequences

### Positive

**For Users with Small Context Windows:**
- ✅ 98% reduction in tool definition context (118K → 2K tokens)
- ✅ More context available for actual work
- ✅ Full functionality still accessible
- ✅ Clear discovery workflow

**For Users with Large Context Windows:**
- ✅ No change - works exactly as before
- ✅ All tools immediately visible (no discovery step)
- ✅ Direct tool calling

**For Development:**
- ✅ Single codebase
- ✅ Single deployment
- ✅ Easy configuration (one env var)
- ✅ No breaking changes
- ✅ Maintains all existing tools

**For Maintenance:**
- ✅ Tool modules unchanged
- ✅ Clear separation of concerns
- ✅ Easy to add new tools

### Negative

**For Dynamic Mode Users:**
- ⚠️ 2-3 step workflow vs direct calling
- ⚠️ Requires learning new meta-tools
- ⚠️ Slightly higher latency (dynamic import)
- ⚠️ Tool registry must be kept in sync

**For Development:**
- ⚠️ Need to maintain tool registry
- ⚠️ Two execution paths to test
- ⚠️ More complex server initialization

### Neutral

- Tool registry can be auto-generated from modules
- Dynamic mode primarily for Claude Desktop and similar
- HTTP deployment typically uses full mode
- Both modes use same underlying API implementation

## Migration Strategy

### For Existing Users
**No action required** - Default mode is "full" (current behavior)

### For New Users with Small Contexts

**Option 1: Environment Variable**
```bash
export FMG_TOOL_MODE=dynamic
python -m fortimanager_mcp
```

**Option 2: .env File**
```bash
echo "FMG_TOOL_MODE=dynamic" >> .env
```

**Option 3: Docker**
```yaml
# docker-compose.yml
environment:
  - FMG_TOOL_MODE=dynamic
```

**Option 4: Claude Desktop Config**
```json
{
  "mcpServers": {
    "fortimanager": {
      "command": "docker",
      "args": [
        "run", "--rm", "-i",
        "-e", "FMG_TOOL_MODE=dynamic",
        "-e", "FORTIMANAGER_HOST=...",
        "fortimanager-mcp"
      ]
    }
  }
}
```

## Testing Strategy

### Unit Tests
- Tool registry search functionality
- Tool metadata retrieval
- Configuration validation

### Integration Tests
Both modes must pass all existing tests:

**Full Mode:**
```bash
FMG_TOOL_MODE=full pytest tests/
```

**Dynamic Mode:**
```bash
FMG_TOOL_MODE=dynamic pytest tests/
```

### Manual Testing
1. Test full mode with all tools
2. Test dynamic mode discovery workflow
3. Test tool execution in both modes
4. Verify context consumption in Claude Desktop

## Performance Implications

### Context Window Usage

**Full Mode:**
- Tool definitions: ~118,000 tokens
- Available for work: Context size - 118,000

**Dynamic Mode:**
- Tool definitions: ~2,000 tokens (meta-tools)
- Available for work: Context size - 2,000
- **Savings: 116,000 tokens (98% reduction)**

### Execution Latency

**Full Mode:**
- Tool call: Instant (already loaded)
- Typical: <100ms

**Dynamic Mode:**
- First call to a tool: Module import + execution
- Typical: <500ms (module import overhead)
- Subsequent calls: Cached in Python, similar to full mode
- Acceptable for interactive use

### Memory Usage

**Full Mode:**
- All modules loaded: ~50-100MB
- Static throughout server lifetime

**Dynamic Mode:**
- Initial: ~5-10MB (meta-tools only)
- Grows as tools are used: Up to same as full mode
- Python caches imported modules

## Documentation Updates

### README.md
- Add section on tool loading modes
- Explain when to use each mode
- Update Claude Desktop configuration examples

### User Guide
- Add dynamic mode workflow guide
- Provide usage examples
- Troubleshooting section

### Docker Documentation
- Add environment variable documentation
- Provide docker-compose examples for both modes

## Future Enhancements

### Potential Improvements
1. **Smart Registry Generation:** Auto-generate registry from tool modules
2. **Tool Preloading:** Option to preload specific categories
3. **Usage Analytics:** Track which tools are most used
4. **Cache Warming:** Pre-import commonly used tools
5. **Hybrid Mode:** Load core tools + dynamic loading for others

### Registry Automation
Currently the tool registry is manually maintained. Future enhancement:
```python
# Auto-generate registry at build time
python -m fortimanager_mcp.utils.generate_registry
```

This would introspect all tool modules and generate `tool_registry.py` automatically.

## Monitoring

### Metrics to Track
- Mode usage distribution (full vs dynamic)
- Tool execution frequency in dynamic mode
- Average execution latency by mode
- Context window consumption

### Health Check
Updated health check shows current mode:
```json
{
  "status": "healthy",
  "mode": "dynamic",
  "tools": "5 meta-tools + 590 on-demand"
}
```

## Success Criteria

**Must Have:**
- ✅ Both modes pass all existing tests
- ✅ No breaking changes for existing users
- ✅ Context reduction >90% in dynamic mode
- ✅ Full functionality in both modes
- ✅ Documentation complete

**Nice to Have:**
- ✅ Dynamic mode execution <500ms overhead
- ✅ Clear error messages in dynamic mode
- ✅ Usage examples for both modes

## Related ADRs
- ADR-001: Python + FastMCP Framework
- ADR-003: Streamable HTTP Client (supports stateless operation)
- ADR-005: Tool Categorization (basis for discovery categories)

## References
- [MCP-Zero: Dynamic Tool Retrieval](https://arxiv.org/abs/2506.01056)
- [ScaleMCP: Auto-Synchronizing Tool Storage](https://arxiv.org/abs/2505.06416)
- [MCP Best Practices: Tool Design](https://www.speakeasy.com/mcp/tool-design/less-is-more)
- [FastMCP Dynamic Tool Management](https://docs.fastmcp.com/tools)

## Revision History
- 2025-10-17: Initial version - Dynamic tool loading implementation

