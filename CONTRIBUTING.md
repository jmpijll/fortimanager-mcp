# Contributing to FortiManager MCP Server

Thank you for your interest in contributing! This guide summarizes how to develop, test, and submit changes.

## Code of Conduct

Please read our [Code of Conduct](CODE_OF_CONDUCT.md) and follow it in all interactions.

## Development Setup

- Python 3.12+
- Docker and Docker Compose
- `uv` for dependency management

Steps:

1. Clone and install dependencies:
   ```bash
   git clone https://github.com/jmpijll/fortimanager-mcp.git
   cd fortimanager-mcp
   uv sync
   ```
2. Create `.env` from `env.example` and set FortiManager credentials.
3. Run the server locally:
   ```bash
   uv run python -m fortimanager_mcp
   ```

## Code Standards

- PEP 8, type hints for all functions
- Prefer async/await for I/O
- Use Pydantic for request/response models
- Single‑purpose MCP tools; clear docstrings (LLMs read these)

## Testing

- Integration tests only; non‑intrusive and read‑only when possible
- Use prefix `MCP_TEST_` for any temporary objects and clean up
- Load credentials from environment variables; never commit secrets

Run tests:
```bash
uv run pytest tests/integration/
```

## Tool Implementation Workflow

1. Research API operation and parameters
2. Implement API client method in `src/fortimanager_mcp/api/`
3. Add MCP tool in `src/fortimanager_mcp/tools/`
4. Add docstrings and examples; handle errors meaningfully
5. Add/adjust tests and docs

## Pull Requests

Before submitting:

- Run tests and linters
- Update docs and CHANGELOG if needed

Submit:

1. Create a feature branch
2. Commit with descriptive messages
3. Push and open a PR using the template

## Issue Reporting

- Use templates for bugs, features, and testing reports
- Include steps to reproduce and environment details

## Security

See our [Security Policy](SECURITY.md) for reporting vulnerabilities.

## License

By contributing, you agree your contributions are MIT‑licensed.


