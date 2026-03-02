# FortiManager MCP Server (DEPRECATED)

> **This repository has been deprecated and archived.**
> 
> It has been replaced by **[fortimanager-code-mode-mcp](https://github.com/jmpijll/fortimanager-code-mode-mcp)**, which uses a fundamentally better architecture (Code Mode pattern with just 2 tools instead of 590+).

---

## Why was this replaced?

The original approach of exposing 590+ individual MCP tools had several problems:

- **Context window bloat** — 118K+ tokens just for tool definitions
- **LLM confusion** — Too many similar tools made it hard for LLMs to choose correctly
- **Maintenance burden** — Every API change required updating dozens of Python modules

The new **Code Mode** architecture solves all of these by using just 2 tools (`search` + `execute`) with a QuickJS WASM sandbox. The LLM writes JavaScript to search the API spec or execute live JSON-RPC calls, giving it full flexibility with minimal context usage.

## Migration

Switch to the new server:

```bash
git clone https://github.com/jmpijll/fortimanager-code-mode-mcp.git
cd fortimanager-code-mode-mcp
npm install && npm run build
```

See the [new repo's README](https://github.com/jmpijll/fortimanager-code-mode-mcp#readme) for full setup instructions.

## License

MIT
