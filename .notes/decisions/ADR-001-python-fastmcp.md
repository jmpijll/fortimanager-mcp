# ADR-001: Python + FastMCP Framework Selection

## Status
Accepted

## Context
We need to build a Model Context Protocol (MCP) server to expose FortiManager JSON RPC API operations. The choice of programming language and MCP framework will impact development speed, maintainability, and deployment options.

## Decision
Use **Python 3.12+** with the **FastMCP framework** for implementing the MCP server.

## Rationale

### Python Selection
1. **Ecosystem**: Rich ecosystem with excellent libraries for HTTP clients (httpx), async I/O, and data validation (Pydantic)
2. **Async Support**: Native async/await support for efficient I/O-bound operations
3. **Developer Experience**: Readable syntax, strong typing with type hints, excellent tooling
4. **API Integration**: Extensive experience with REST/JSON-RPC APIs in Python
5. **Deployment**: Well-established Docker patterns and deployment practices

### FastMCP Framework Selection
1. **Official Support**: Part of the Model Context Protocol official Python SDK
2. **Simplicity**: High-level API simplifies MCP server development
3. **Starlette Integration**: Built on Starlette ASGI framework, enabling easy deployment
4. **Transport Options**: Supports both stdio and streamable-http transports
5. **Stateless Mode**: Supports stateless_http mode ideal for containerized deployment
6. **Documentation**: Well-documented with examples and code snippets
7. **Active Development**: Maintained by the MCP team

### Alternatives Considered

#### TypeScript/Node.js
- **Pros**: Official MCP TypeScript SDK, strong ecosystem
- **Cons**: Less familiar for the team, async patterns more complex, heavier runtime

#### Low-level MCP Python SDK
- **Pros**: More control, lighter weight
- **Cons**: More boilerplate code, longer development time, need to handle more low-level details

#### Rust MCP SDK
- **Pros**: Performance, type safety
- **Cons**: Steeper learning curve, longer development time, overkill for I/O-bound application

## Consequences

### Positive
- Fast development with high-level FastMCP API
- Easy integration with existing Python tools and libraries
- Straightforward Docker deployment
- Excellent async I/O performance for API calls
- Strong typing and validation with Pydantic
- Simple HTTP transport for production use

### Negative
- Python runtime overhead (minimal for I/O-bound workload)
- Dependency on FastMCP framework evolution
- Need to manage Python package dependencies

### Neutral
- Python 3.12 requirement (modern but widely available)
- Learning FastMCP patterns (quick due to good documentation)

## Implementation Notes
- Use `uv` for fast, reliable dependency management
- Pin FastMCP to `>=1.0.0` for stability
- Use type hints throughout for better IDE support and validation
- Follow async/await patterns for all I/O operations
- Leverage Pydantic v2 for data validation and serialization

## References
- [Model Context Protocol Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [FastMCP Documentation](https://modelcontextprotocol.io/docs/python-sdk/fastmcp)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [Pydantic V2](https://docs.pydantic.dev/)

