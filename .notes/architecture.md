# FortiManager MCP Server - Architecture

## System Architecture

### High-Level Components

```
┌──────────────────────────────────────────────────────────────┐
│                        MCP Client Layer                       │
│           (AI Assistants: Claude, Cursor, etc.)              │
└───────────────────────────┬──────────────────────────────────┘
                            │
                            │ Streamable HTTP
                            │ (MCP Protocol)
                            │
┌───────────────────────────▼──────────────────────────────────┐
│                    MCP Server (FastMCP)                       │
├───────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │ Device Tools │  │ Object Tools │  │ Policy Tools │       │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘       │
│         │                  │                  │                │
│  ┌──────▼──────────────────▼──────────────────▼───────┐      │
│  │           MCP Tool Registration Layer              │      │
│  └──────┬─────────────────────────────────────────────┘      │
│         │                                                      │
│  ┌──────▼──────────────────────────────────────────────┐     │
│  │            Configuration Management                  │     │
│  │        (Settings, Logging, Error Handling)          │     │
│  └──────┬───────────────────────────────────────────────┘    │
└─────────┼────────────────────────────────────────────────────┘
          │
          │
┌─────────▼────────────────────────────────────────────────────┐
│              FortiManager API Client Layer                    │
├───────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │ Auth Handler │  │ HTTP Client  │  │ Error Parser │       │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘       │
│         │                  │                  │                │
│  ┌──────▼──────────────────▼──────────────────▼───────┐      │
│  │           Base API Client (JSON-RPC)               │      │
│  └──────┬─────────────────────────────────────────────┘      │
│         │                                                      │
│  ┌──────▼──────────────────────────────────────────────┐     │
│  │         Domain-Specific API Modules                  │     │
│  │  - devices.py  - adoms.py    - objects.py           │     │
│  │  - policies.py - install.py  - monitoring.py        │     │
│  └──────┬───────────────────────────────────────────────┘    │
└─────────┼────────────────────────────────────────────────────┘
          │
          │ HTTPS (JSON-RPC)
          │
┌─────────▼────────────────────────────────────────────────────┐
│                      FortiManager                             │
│                   JSON RPC API Endpoint                       │
│                  POST https://{host}/jsonrpc                  │
└───────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. MCP Server Layer
**Responsibility**: Expose FortiManager operations as MCP tools

**Key Components**:
- `server.py`: FastMCP server initialization and configuration
- Tool registration and schema definition
- Request/response handling
- Lifespan management (startup/shutdown)

**Technologies**:
- FastMCP framework
- Starlette ASGI application
- Uvicorn server

### 2. MCP Tools Layer
**Responsibility**: Define individual MCP tools for FortiManager operations

**Organization**:
- `device_tools.py`: Device management tools
- `object_tools.py`: Firewall object tools
- `policy_tools.py`: Policy management tools
- `monitoring_tools.py`: Monitoring and task tools

**Each Tool Provides**:
- Input schema (Pydantic model)
- Output schema (structured response)
- Comprehensive description for LLM understanding
- Error handling

### 3. FortiManager API Client Layer
**Responsibility**: Abstract FortiManager JSON-RPC API interactions

**Key Components**:

#### Base Client (`client.py`)
- JSON-RPC request construction
- HTTP client with connection pooling
- Retry logic for transient failures
- Response parsing and validation

#### Authentication (`auth.py`)
- Token-based authentication (primary)
- Session-based authentication (fallback)
- Automatic token refresh
- Session lifecycle management

#### Domain Modules
- `devices.py`: Device CRUD, settings management
- `adoms.py`: ADOM operations
- `objects.py`: Firewall objects (addresses, services, etc.)
- `policies.py`: Policy package and rule management
- `installation.py`: Install operations (device/package)
- `monitoring.py`: Task monitoring, system status

### 4. Data Models
**Responsibility**: Type-safe data structures

**Implementation**: Pydantic v2 models
- Request/response models
- Configuration settings
- Domain entities (Device, ADOM, Policy, etc.)
- Validation and serialization

### 5. Configuration & Utilities
**Responsibility**: Cross-cutting concerns

**Components**:
- `config.py`: Environment-based configuration
- `errors.py`: Custom exception hierarchy
- Logging configuration
- Health check endpoints

## Data Flow

### Typical Request Flow
```
1. AI Assistant → MCP Request → MCP Server
2. MCP Server → Parse Tool Call → Validate Input
3. MCP Server → API Client → Build JSON-RPC Request
4. API Client → Authenticate → Add Session/Token
5. API Client → HTTP Request → FortiManager
6. FortiManager → Process → HTTP Response
7. API Client → Parse Response → Validate
8. API Client → Return Data → MCP Server
9. MCP Server → Format Response → AI Assistant
```

### Error Handling Flow
```
1. Exception Raised in API Client
2. Parse FortiManager Error Code
3. Map to Custom Exception Type
4. Add Context (request details, URL)
5. Log Error with Details
6. Return Structured Error to MCP Layer
7. MCP Server Formats for Client
8. AI Assistant Receives Human-Readable Error
```

## Security Considerations

### Authentication
- API tokens stored in environment variables
- Never log sensitive credentials
- Support for SSL/TLS verification
- Secure token transmission

### API Access
- Read-only operations preferred
- Destructive operations require explicit confirmation
- Rate limiting considerations
- Audit logging

### Docker Security
- Non-root user in container
- Minimal base image (Python slim)
- No secrets in image layers
- Environment-based configuration

## Scalability Considerations

### Stateless Design
- No server-side session storage
- Each request is independent
- Horizontal scaling possible

### Connection Pooling
- Reuse HTTP connections
- Configurable pool size
- Connection timeout handling

### Async I/O
- Non-blocking API calls
- Concurrent request handling
- Efficient resource utilization

## Deployment Architecture

### Docker Compose Deployment
```
┌─────────────────────────────────────┐
│         Docker Host                 │
│                                     │
│  ┌───────────────────────────────┐ │
│  │  fortimanager-mcp Container   │ │
│  │                               │ │
│  │  ┌─────────────────────────┐ │ │
│  │  │   MCP Server (Port 8000) │ │ │
│  │  └─────────────────────────┘ │ │
│  │                               │ │
│  │  Volumes:                     │ │
│  │  - ./logs:/app/logs          │ │
│  │                               │ │
│  │  Environment:                 │ │
│  │  - FORTIMANAGER_HOST         │ │
│  │  - FORTIMANAGER_API_TOKEN    │ │
│  └───────────────┬───────────────┘ │
│                  │                  │
└──────────────────┼──────────────────┘
                   │
                   │ HTTPS
                   ▼
          ┌─────────────────┐
          │  FortiManager   │
          └─────────────────┘
```

## Integration Points

### MCP Client Integration
Clients can connect using:
- Streamable HTTP transport: `http://localhost:8000/mcp`
- Standard MCP protocol

### FortiManager Integration
- Endpoint: `https://{host}/jsonrpc`
- Authentication: Token header or session ID
- Protocol: JSON-RPC 2.0

## Testing Strategy

### Integration Testing
- Real FortiManager instance required
- Non-intrusive operations (read-only preferred)
- Test object naming convention: "MCP_TEST_*"
- Automatic cleanup after tests
- Credentials from environment variables

### Test Coverage
- All API client modules
- Critical MCP tools
- Authentication flows
- Error handling paths

## Performance Considerations

### Response Time
- Target: < 2s for typical operations
- Task monitoring: Polling with exponential backoff
- Connection reuse for efficiency

### Resource Usage
- Memory: ~100MB base
- CPU: Minimal (I/O bound)
- Network: Depends on FortiManager latency

## Monitoring & Observability

### Logging
- Structured logging (JSON format)
- Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
- Request/response logging (sanitized)
- Performance metrics

### Health Checks
- HTTP endpoint: `/health`
- FortiManager connectivity check
- Configuration validation

### Metrics
- Request count by tool
- Error rates
- Response times
- Authentication failures

