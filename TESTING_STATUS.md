# Testing Status

**Version:** 0.1.0-beta  
**Last Updated:** October 16, 2025

---

## Overview

This document tracks the testing status of all 590 MCP tools in the FortiManager MCP Server. The project is currently in **beta** status, with comprehensive production testing ongoing.

---

## Testing Categories

### Tested in Production
**Status:** Validated in real FortiManager environments  
**Count:** ~200 tools

These tools have been tested and validated in production FortiManager environments:

**Device Management (Early Implementation)**
- Device listing and retrieval
- Device group operations
- Basic VDOM operations
- Device metadata
- Firmware listing

**Provisioning & Templates (Core Operations)**
- Template listing and retrieval
- CLI template operations
- Basic provisioning operations

**Policy Management (Core Operations)**
- Policy package listing
- Firewall policy CRUD
- Policy installation (basic)
- Central NAT operations

**Objects Management (Core Operations)**
- Address and address group CRUD
- Service CRUD
- Basic object operations

**ADOM Management (Core Operations)**
- ADOM listing
- Workspace locking/unlocking
- Basic ADOM operations

**System Operations (Core)**
- System status retrieval
- Basic monitoring
- Configuration retrieval

---

### Syntax Validated
**Status:** Type-checked, linter-verified, builds successfully  
**Count:** 590 tools (all tools)

All tools have passed:
- Python type checking (mypy)
- Linter validation (ruff)
- Import verification
- Docker build process
- Code review

---

### Requires Production Testing
**Status:** Not yet validated in production environments  
**Count:** ~390 tools

These tools require comprehensive production testing:

**Advanced Device Operations**
- HA cluster advanced operations
- FortiAP/FortiSwitch/FortiExtender management
- Device blueprint operations
- Advanced firmware operations
- Device certificate management
- Vulnerability scanning
- RMA operations

**Advanced Provisioning**
- SD-WAN templates
- IPsec tunnel templates
- Certificate templates
- Static route templates
- Advanced FortiAP/FortiSwitch operations
- Template groups
- Pre-run validations

**Advanced Policy Operations**
- Policy blocks
- Scheduled installations
- Install previews
- Policy sections
- Policy positioning
- Global policy packages
- Offline installation
- Device DB-only installation

**Advanced Object Operations**
- Object metadata operations
- Where-used analysis
- Zone management
- Virtual wire pairs
- Internet service FQDNs
- Normalized interfaces
- Replacement message groups

**Advanced ADOM Operations**
- ADOM cloning
- Device movement between ADOMs
- Revision management
- ADOM checksums and integrity
- Resource limits
- Display preferences

**Security Profiles (Advanced)**
- Batch operations (add/update/delete)
- Profile entry validation
- Entry count operations
- IPS advanced queries
- DLP advanced queries

**FortiGuard (Advanced)**
- Update operations
- Package versions
- Object import/export
- Upstream server operations

**Monitoring & Tasks (Advanced)**
- Task history
- Performance statistics
- Detailed log statistics
- Bandwidth monitoring
- Session statistics
- Alert history
- Configuration changes

**Installation & Updates (Advanced)**
- Abort operations
- Installation history
- Validation operations
- Progress tracking
- Dependencies
- Rollback operations

**VPN (Advanced)**
- IPsec concentrators
- FortiClient templates
- Manual-key interfaces
- Tunnel monitoring
- VPN statistics

**SD-WAN (Advanced)**
- Advanced zone operations
- Health check details
- Service configurations
- Member management
- Traffic classes

**System (Advanced)**
- Certificate operations
- TACACS+ servers
- User sessions
- Backup/restore
- API user details
- FortiGuard upstream servers

**Specialized Operations**
- Connector management
- Meta fields
- Security Fabric (CSF)
- Subscription fetch
- FortiManager Cloud
- Docker management
- Database cache
- System proxy
- QoS management

---

## Testing Methodology

### Production Testing Approach

For each tool requiring testing:

1. **Environment Setup**
   - Use non-production FortiManager instance
   - Create test ADOM
   - Set up test devices (if applicable)
   - Configure appropriate permissions

2. **Test Execution**
   - Execute tool with valid parameters
   - Verify expected behavior
   - Check FortiManager logs
   - Validate return values
   - Test error conditions

3. **Documentation**
   - Record test results
   - Document any issues
   - Note FortiManager version tested
   - Document prerequisites

4. **Validation**
   - Verify no unintended side effects
   - Confirm operation reversibility (where applicable)
   - Check system stability
   - Validate audit logs

---

## Testing Priority

### High Priority (Business Critical)
Tools that perform write operations or system changes:
- Device provisioning
- Policy installation
- Configuration changes
- System operations

### Medium Priority (Operational)
Tools that perform read operations with complex logic:
- Advanced queries
- Statistical operations
- Monitoring operations

### Low Priority (Informational)
Tools that perform simple read operations:
- List operations
- Status checks
- Basic retrieval

---

## Reporting Issues

If you discover issues during testing:

1. **Check Prerequisites**
   - FortiManager version compatibility
   - API user permissions
   - Network connectivity
   - Authentication configuration

2. **Gather Information**
   - Tool name and parameters used
   - Expected vs actual behavior
   - Error messages
   - FortiManager logs
   - MCP server logs

3. **Report via GitHub Issues**
   - Use issue template
   - Include reproduction steps
   - Attach relevant logs (sanitized)
   - Note FortiManager version

---

## Testing Progress

**Target:** 100% production testing coverage  
**Current:** ~34% (200/590 tools)  
**Status:** Ongoing

### Milestone Goals

**0.2.0-beta** (Target: Q4 2025)
- 50% tools production tested
- All high-priority tools validated
- Bug fixes from community feedback

**0.3.0-beta** (Target: Q1 2026)
- 75% tools production tested
- All medium-priority tools validated
- Performance optimization

**1.0.0** (Target: Q2 2026)
- 100% tools production tested
- Complete validation across FortiManager versions
- Production-ready stable release

---

## Contributing to Testing

Community testing contributions are welcome:

1. **Test Against Your Environment**
   - Use non-production FortiManager
   - Test tools relevant to your use case
   - Document results

2. **Report Results**
   - Submit successful test reports
   - Report any issues found
   - Share use case examples

3. **Expand Test Coverage**
   - Test against different FMG versions
   - Test with different configurations
   - Validate edge cases

---

## Testing Resources

**Documentation:**
- `.notes/QUICK_REFERENCE.md` - Common operations guide
- `.notes/api_coverage_map.md` - Complete tool listing
- `.notes/PROJECT_STATUS.md` - Implementation details

**Test Environment:**
- Docker deployment for testing
- Integration test framework
- Non-intrusive test examples

---

*This is a beta release. Production testing is ongoing. Please test thoroughly in non-production environments before production use.*


