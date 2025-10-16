# FortiManager MCP Server - Directory Structure

```
fortimanager-mcp/
├── .cursorrules                    # Cursor IDE AI guidelines
├── .cursorignore                   # Files to exclude from AI context
├── .dockerignore                   # Files to exclude from Docker build
├── .env.example                    # Example environment variables
├── .gitignore                      # Git ignore rules
├── docker-compose.yml              # Docker Compose configuration
├── Dockerfile                      # Docker build instructions
├── pyproject.toml                  # Python project configuration
├── README.md                       # Project documentation
│
├── .notes/                         # Project documentation and notes
│   ├── project_overview.md         # High-level project description
│   ├── architecture.md             # System architecture documentation
│   ├── task_list.md                # Development task tracking
│   ├── directory_structure.md      # This file
│   └── decisions/                  # Architecture Decision Records (ADRs)
│       ├── ADR-001-python-fastmcp.md
│       ├── ADR-002-token-auth.md
│       ├── ADR-003-streamable-http.md
│       ├── ADR-004-integration-testing.md
│       └── ADR-005-tool-categorization.md
│
├── docs/                           # Generated documentation
│   ├── api/                        # API reference
│   ├── tools/                      # Tool catalog
│   └── guides/                     # User guides
│
├── logs/                           # Application logs (created at runtime)
│   └── fortimanager-mcp.log
│
├── src/                            # Source code
│   └── fortimanager_mcp/           # Main package
│       ├── __init__.py             # Package initialization
│       ├── __main__.py             # Entry point for module execution
│       ├── server.py               # MCP server implementation
│       │
│       ├── api/                    # FortiManager API client
│       │   ├── __init__.py
│       │   ├── auth.py             # Authentication handlers
│       │   ├── client.py           # Base JSON-RPC client
│       │   ├── models.py           # Pydantic data models
│       │   ├── devices.py          # Device management API
│       │   ├── adoms.py            # ADOM management API
│       │   ├── objects.py          # Firewall objects API
│       │   ├── policies.py         # Policy management API
│       │   ├── installation.py     # Installation operations API
│       │   └── monitoring.py       # Monitoring and task API
│       │
│       ├── tools/                  # MCP tool definitions
│       │   ├── __init__.py
│       │   ├── device_tools.py     # Device management tools
│       │   ├── object_tools.py     # Firewall object tools
│       │   ├── policy_tools.py     # Policy management tools
│       │   └── monitoring_tools.py # Monitoring tools
│       │
│       └── utils/                  # Utilities and helpers
│           ├── __init__.py
│           ├── config.py           # Configuration management
│           └── errors.py           # Custom exception classes
│
├── tests/                          # Test suite
│   ├── __init__.py
│   ├── integration/                # Integration tests
│   │   ├── __init__.py
│   │   ├── conftest.py             # Pytest fixtures and configuration
│   │   ├── test_devices.py         # Device API integration tests
│   │   ├── test_adoms.py           # ADOM API integration tests
│   │   ├── test_objects.py         # Objects API integration tests
│   │   ├── test_policies.py        # Policies API integration tests
│   │   ├── test_monitoring.py      # Monitoring API integration tests
│   │   └── test_tools.py           # MCP tools integration tests
│   │
│   └── data/                       # Test data and fixtures
│       ├── sample_responses.json   # Sample API responses
│       └── test_configs.yaml       # Test configurations
│
└── FortiManager-how-to-guide/      # Reference documentation (read-only)
    └── ...                         # FortiManager API documentation
```

## Directory Purposes

### Root Level
- Configuration files for tools and deployment
- Docker-related files
- Main documentation (README)

### `.notes/`
- Project management documentation
- Architecture decisions (ADRs)
- Task tracking
- Internal knowledge base

### `docs/`
- Generated user-facing documentation
- API references
- Usage guides
- Deployment instructions

### `logs/`
- Runtime logs (not in git)
- Created automatically by the application
- Mounted as Docker volume

### `src/fortimanager_mcp/`
Main application code following domain-driven design:

#### `api/`
- Low-level FortiManager API client
- Domain-specific modules for each API area
- JSON-RPC implementation
- Authentication and session management

#### `tools/`
- High-level MCP tool implementations
- Each file contains related tools
- Input/output schema definitions
- LLM-friendly descriptions

#### `utils/`
- Cross-cutting concerns
- Configuration management
- Error handling
- Logging setup

### `tests/`
- Integration tests only (no unit tests)
- Organized by API domain
- Shared fixtures and utilities
- Test data and samples

## Key Files

### Configuration
- `pyproject.toml`: Python dependencies, build config, tool settings
- `.env.example`: Environment variable template
- `docker-compose.yml`: Container orchestration

### Application Entry Points
- `src/fortimanager_mcp/__main__.py`: CLI entry point
- `src/fortimanager_mcp/server.py`: MCP server initialization

### Core Implementations
- `src/fortimanager_mcp/api/client.py`: Base API client
- `src/fortimanager_mcp/server.py`: MCP server setup
- `src/fortimanager_mcp/utils/config.py`: Settings management

## File Naming Conventions

### Python Modules
- Lowercase with underscores: `device_tools.py`
- Descriptive names indicating purpose
- Group related functionality

### Documentation
- Markdown format: `.md`
- Uppercase for root-level: `README.md`
- Lowercase for .notes: `architecture.md`
- ADR prefix for decisions: `ADR-001-topic.md`

### Configuration
- Dotfiles for tools: `.gitignore`, `.env`
- Standard names: `pyproject.toml`, `Dockerfile`

## Import Paths

Examples of how to import from this structure:

```python
# API client
from fortimanager_mcp.api.client import FortiManagerClient
from fortimanager_mcp.api.models import Device, ADOM

# Tools (typically registered, not directly imported)
from fortimanager_mcp.tools.device_tools import list_devices

# Utilities
from fortimanager_mcp.utils.config import Settings
from fortimanager_mcp.utils.errors import FortiManagerError
```

## Volume Mounts (Docker)

```yaml
volumes:
  - ./logs:/app/logs              # Log persistence
  - ./.env:/app/.env:ro           # Configuration (read-only)
```

## Excluded from Git
- `.env` (secrets)
- `__pycache__/`, `*.pyc` (Python cache)
- `.venv/`, `venv/` (virtual environments)
- `logs/` (runtime logs)
- `.pytest_cache/` (test cache)
- `.mypy_cache/` (type checker cache)

## Excluded from Docker Build
- `.git/` (version control)
- `.venv/`, `venv/` (local virtual env)
- `tests/` (not needed in production)
- `docs/` (not needed in production)
- `.notes/` (internal documentation)
- `FortiManager-*-guide/` (reference docs)

