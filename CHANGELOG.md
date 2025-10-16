# Changelog

All notable changes to the FortiManager MCP Server project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0-beta] - 2025-10-16

### Initial Beta Release

This is the initial beta release providing complete coverage of all documented FortiManager 7.4.8 JSON-RPC API operations.

#### Added
- 590 MCP tools implementing 555 documented API operations (100% coverage)
- Complete device management operations (116 operations)
- Complete provisioning & template operations (82 operations)
- Complete policy package management (77 operations)
- Complete object management (61 operations)
- Complete ADOM management (36 operations)
- Complete security profile operations (35 operations)
- Complete FortiManager system operations (30 operations)
- Complete FortiGuard management (28 operations)
- Complete monitoring & task operations (26 operations)
- Complete installation & update operations (20 operations)
- Complete CLI script management (13 operations)
- Complete VPN management (12 operations)
- Complete SD-WAN management (11 operations)
- Complete workspace & locking operations (4 operations)
- Additional specialized operations across 10 categories
- Docker deployment support
- Dual authentication (token-based and session-based)
- Comprehensive documentation
- Type-safe implementation with full type hints
- Zero linter errors

#### Testing Status
- Early implementation tools (approximately 200 tools) tested in production environments
- Remaining tools (approximately 390 tools) require production validation
- All tools validated for syntax and type safety
- Docker build verified
- Integration test framework in place

#### Known Limitations
- Not all tools have been tested in production environments
- Some advanced operations may require additional validation
- Testing against FortiManager versions other than 7.4.8 not yet performed

#### Security
- Token-based authentication recommended
- TLS/HTTPS support
- No credential storage in codebase
- Follows security best practices

#### Documentation
- Complete API coverage map
- Architecture documentation
- Quick reference guide
- Integration examples
- Troubleshooting guide

### Notes

This is a **beta release**. While the implementation is complete and early tools have been production-tested, comprehensive validation of all 590 tools is ongoing. Users should:

1. Test thoroughly in non-production environments first
2. Validate operations against their specific FortiManager configuration
3. Report any issues or bugs via GitHub Issues
4. Follow security best practices (use API tokens, enable SSL verification)

### Next Steps

The project roadmap includes:
- Comprehensive production testing of all 590 tools
- Additional integration tests
- Performance optimization
- Community feedback incorporation
- Move to stable 1.0.0 release after testing completion

---

## Version History

- **0.1.0-beta** (2025-10-16): Initial beta release with complete API coverage

