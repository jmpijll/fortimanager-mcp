# Contributing to FortiManager MCP Server

Thank you for your interest in contributing to the FortiManager MCP Server! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md) to maintain a welcoming and respectful community.

## Development Setup

### Prerequisites

- Python 3.12 or higher
- Docker and Docker Compose
- uv (Python package manager)
- Access to a FortiManager instance (for testing)

### Local Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/jmpijll/fortimanager-mcp.git
   cd fortimanager-mcp
   ```

2. Install dependencies using uv:
   ```bash
   uv sync
   ```

3. Copy the example environment file:
   ```bash
   cp env.example .env
   ```

4. Configure your FortiManager credentials in `.env`:
   ```
   FORTIMANAGER_HOST=your-fortimanager-host
   FORTIMANAGER_USERNAME=your-username
   FORTIMANAGER_PASSWORD=your-password
   ```

5. Test the installation:
   ```bash
   uv run python -m fortimanager_mcp
   ```

## Code Standards

### Python Style Guidelines

- Follow PEP 8 style guidelines
- Use type hints for all function signatures
- Maximum line length: 100 characters
- Use descriptive variable and function names
- Add docstrings to all public functions and classes

### Code Quality

- Write clean, readable, and maintainable code
- Keep functions focused and single-purpose
- Avoid unnecessary complexity
- Use async/await for I/O operations
- Handle errors gracefully with meaningful messages

### Type Safety

- Use Python type hints consistently
- Use Pydantic models for data validation
- Validate all input parameters
- Return typed responses

## Testing Requirements

### Testing Philosophy

All tests must be **non-intrusive** and **read-only** when possible:

- **Prefer**: List operations, get operations, query operations, status checks
- **Avoid**: Create, update, delete, install operations (unless explicitly testing those features)
- **Never**: Modify production systems during testing

### Test Object Naming

If you must create test objects:
- Use "MCP_TEST_" prefix for all test objects
- Clean up test objects after test completion
- Document cleanup procedures in test files

### Running Tests

```bash
# Run integration tests
uv run pytest tests/integration/

# Run specific test file
uv run pytest tests/integration/test_devices.py

# Run with verbose output
uv run pytest -v tests/integration/
```

### Test Coverage

- Integration tests are required (no unit tests with mocks)
- Test real API interactions when safe
- Load credentials from environment variables
- Never commit credentials to the repository

## Tool Implementation Workflow

### Adding New MCP Tools

1. **Research the API Operation**
   - Review FortiManager JSON-RPC API documentation
   - Understand the endpoint, parameters, and response format
   - Check for any prerequisites or dependencies

2. **Implement the API Method**
   - Add method to appropriate module in `src/fortimanager_mcp/api/`
   - Use type hints and Pydantic models
   - Include comprehensive docstring
   - Handle errors appropriately

3. **Create the MCP Tool**
   - Add tool to appropriate module in `src/fortimanager_mcp/tools/`
   - Use `@mcp.tool()` decorator
   - Provide detailed description (LLMs read these!)
   - Validate input parameters
   - Return structured responses

4. **Document the Tool**
   - Update API coverage map if adding new operations
   - Include usage examples in docstrings
   - Document any special considerations

5. **Test the Tool**
   - Write integration tests
   - Test with real FortiManager instance
   - Verify error handling
   - Ensure read-only operations when possible

### Example Tool Implementation

```python
@mcp.tool()
async def list_devices(
    adom: str = "root",
    filter_: Optional[str] = None
) -> dict[str, Any]:
    """
    List all devices in an ADOM.
    
    Args:
        adom: ADOM name (default: "root")
        filter_: Optional filter expression
        
    Returns:
        Dictionary containing device list and metadata
        
    Example:
        List all devices in root ADOM:
        {"adom": "root"}
    """
    try:
        async with get_client() as client:
            devices = await client.list_devices(adom=adom, filter_=filter_)
            return {
                "status": "success",
                "data": devices,
                "count": len(devices)
            }
    except Exception as e:
        return {"status": "error", "message": str(e)}
```

## Pull Request Process

### Before Submitting

1. Ensure your code follows the style guidelines
2. Run tests and verify they pass
3. Update documentation as needed
4. Add your changes to CHANGELOG.md
5. Commit with clear, descriptive messages

### Submitting a Pull Request

1. Fork the repository
2. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. Make your changes and commit:
   ```bash
   git add .
   git commit -m "Add feature: descriptive message"
   ```

4. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

5. Open a pull request on GitHub
6. Fill out the PR template completely
7. Link any related issues

### PR Review Process

- Maintainers will review your PR within 3-5 business days
- Address any requested changes promptly
- Keep discussions professional and constructive
- Once approved, your PR will be merged

## Issue Reporting Guidelines

### Bug Reports

Use the Bug Report template and include:
- Clear description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Environment details (Python version, OS, etc.)
- Relevant logs or error messages

### Feature Requests

Use the Feature Request template and include:
- Clear description of the feature
- Use case and motivation
- Proposed implementation (if applicable)
- Alternatives considered

### Testing Reports

Use the Testing Report template to:
- Report tool functionality verification
- Share test results and findings
- Contribute to production testing efforts

## Documentation Requirements

### Code Documentation

- Add docstrings to all public functions and classes
- Include parameter descriptions and types
- Provide usage examples
- Document exceptions that may be raised

### API Documentation

- Update `.notes/api_coverage_map.md` when adding operations
- Keep coverage statistics accurate
- Document any API limitations or quirks

### User Documentation

- Update README.md for user-facing changes
- Add examples for new features
- Keep installation instructions current

## Project Structure

```
fortimanager-mcp/
├── src/fortimanager_mcp/
│   ├── api/              # FortiManager API client methods
│   ├── tools/            # MCP tool implementations
│   ├── utils/            # Utilities and configuration
│   └── server.py         # FastMCP server setup
├── tests/
│   └── integration/      # Integration tests
├── .github/              # GitHub templates and workflows
└── .notes/              # Technical documentation
```

## Communication

### Getting Help

- Open a discussion on GitHub for questions
- Use issues for bug reports and feature requests
- Join community discussions

### Reporting Security Issues

Please review our [Security Policy](SECURITY.md) for reporting security vulnerabilities.

## License

By contributing to this project, you agree that your contributions will be licensed under the MIT License.

## Recognition

Contributors will be recognized in:
- GitHub contributors list
- Release notes for significant contributions
- Project acknowledgments

Thank you for contributing to FortiManager MCP Server!

