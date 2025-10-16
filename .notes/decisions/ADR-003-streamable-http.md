# ADR-003: Streamable-HTTP Transport for Docker Deployment

## Status
Accepted

## Context
The Model Context Protocol (MCP) supports multiple transport mechanisms:
1. **stdio (Standard I/O)**: Process-based communication, client spawns server as subprocess
2. **SSE (Server-Sent Events)**: HTTP-based with SSE for server-to-client messages
3. **Streamable-HTTP**: Newer HTTP-based transport combining request/response with streaming

We need to choose a transport that works well with Docker deployment and production environments.

## Decision
Use **Streamable-HTTP** transport in **stateless mode** for the MCP server.

## Rationale

### Streamable-HTTP Advantages

#### Production-Ready
1. **HTTP-Based**: Standard HTTP protocol, works with load balancers, reverse proxies
2. **Firewall-Friendly**: Uses standard HTTP ports (8000), no special network configuration
3. **Debuggable**: Can inspect traffic with standard HTTP tools (curl, Postman, browser dev tools)
4. **Stateless Option**: Supports stateless mode for true RESTful behavior

#### Docker-Friendly
1. **Port Mapping**: Simple Docker port exposure (`-p 8000:8000`)
2. **Health Checks**: Easy to implement HTTP health check endpoints
3. **Load Balancing**: Can run multiple containers behind a load balancer
4. **Horizontal Scaling**: Stateless design enables easy horizontal scaling

#### Integration Benefits
1. **Client Compatibility**: Works with any HTTP client
2. **CORS Support**: Can configure CORS for browser-based clients
3. **Authentication**: Standard HTTP authentication mechanisms
4. **Monitoring**: Compatible with standard HTTP monitoring tools

### Why Not stdio?

#### stdio Disadvantages
- Requires client to spawn server as subprocess
- Not suitable for shared server instances
- Can't run in Docker as a long-lived service
- Complex lifecycle management
- No remote access support

#### stdio Advantages (not applicable to our use case)
- Lower latency (process-local communication)
- Simpler for desktop app integration
- No network configuration needed

### Why Not SSE?

#### SSE vs Streamable-HTTP
- SSE is the predecessor to Streamable-HTTP
- Streamable-HTTP is the recommended modern approach
- Both are HTTP-based, but Streamable-HTTP has better semantics
- FastMCP defaults to Streamable-HTTP for `transport="streamable-http"`

### Stateless Mode

We use `stateless_http=True` in FastMCP:

```python
mcp = FastMCP(
    "FortiManager API Server",
    stateless_http=True  # No session persistence
)
```

#### Stateless Benefits
1. **Scalability**: Each request is independent
2. **Reliability**: No session state to lose on restart
3. **Simplicity**: No session management code needed
4. **Cloud-Native**: Perfect for Kubernetes/Docker Swarm

#### Stateless Considerations
- Each request must include full context
- No server-side caching between requests
- FortiManager authentication handled per-request (token-based)

## Configuration

### Server Configuration
```python
# server.py
if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",  # Bind to all interfaces (Docker)
        port=8000
    )
```

### Docker Deployment
```yaml
# docker-compose.yml
services:
  fortimanager-mcp:
    ports:
      - "8000:8000"
    environment:
      - MCP_SERVER_PORT=8000
      - MCP_SERVER_HOST=0.0.0.0
```

### Client Connection
```
http://localhost:8000/mcp
```

## Consequences

### Positive
- Simple Docker deployment with port mapping
- Can run multiple server instances
- Standard HTTP tooling for debugging and monitoring
- Easy to integrate with reverse proxies (nginx, Traefik)
- Health check endpoint for orchestration
- Works with Kubernetes, Docker Swarm, etc.

### Negative
- Slightly higher latency than stdio (network overhead)
- Requires HTTP server infrastructure
- Need to configure CORS if accessed from browsers

### Neutral
- Must handle HTTP-specific concerns (timeouts, keep-alive)
- Network security considerations (TLS, authentication)

## Implementation Notes

### Health Check Endpoint
```python
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "fortimanager-mcp"}
```

### CORS Configuration
```python
from starlette.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Uvicorn Server
FastMCP uses Uvicorn internally:
- ASGI server for async Python
- Production-ready
- Supports graceful shutdown
- Configurable workers for performance

## Deployment Patterns

### Single Container
```bash
docker-compose up
# Server at http://localhost:8000/mcp
```

### Behind Reverse Proxy
```nginx
location /mcp/ {
    proxy_pass http://fortimanager-mcp:8000/;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Host $host;
}
```

### Kubernetes Deployment
```yaml
apiVersion: v1
kind: Service
metadata:
  name: fortimanager-mcp
spec:
  ports:
  - port: 8000
    targetPort: 8000
  selector:
    app: fortimanager-mcp
```

## Future Considerations
- Add TLS/HTTPS support for production
- Implement rate limiting
- Add request authentication for MCP layer
- Consider WebSocket transport if added to MCP spec

## References
- [MCP Streamable-HTTP Transport](https://modelcontextprotocol.io/docs/concepts/transports#streamable-http)
- [FastMCP Transport Configuration](https://modelcontextprotocol.io/docs/python-sdk/fastmcp#transport)
- [Uvicorn Documentation](https://www.uvicorn.org/)
- [Starlette Framework](https://www.starlette.io/)

