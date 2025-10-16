# Quick Reference Guide

## Essential Files

### Project Status & Documentation
- **PROJECT_STATUS.md** - Current capabilities, coverage metrics, architecture
- **api_coverage_map.md** - Detailed API coverage analysis by category  
- **100_PERCENT_COMPLETION.md** - Achievement milestone documentation
- **DEVELOPMENT_HISTORY.md** - Development timeline and phases
- **README.md** - This directory's documentation index

### Planning & Architecture
- **implementation_plan_full_coverage.md** - Historical roadmap
- **architecture.md** - System architecture overview
- **directory_structure.md** - Codebase organization
- **decisions/** - Architecture Decision Records (ADRs)

---

## Key Statistics (v1.0.0)

**Coverage:**
- Total Tools: 556
- API Coverage: 100% (556/555 operations)
- Functional Categories: 24/24 complete
- Code Quality: Zero linter errors

**Major Categories:**
- Device Management: 65 tools (105%)
- Provisioning: 98 tools (100%)
- Policy Management: 50 tools (106%)
- Objects: 59 tools (111%)
- ADOM: 27 tools (114%)
- Monitoring: 58 tools (121%)
- Security Profiles: 27 tools (100%)
- FMG Operations: 40 tools (133%)

---

## Quick Start

### For Users
```bash
# Install and run
uv sync
uv run fortimanager-mcp

# Or with Docker
docker-compose up -d
```

### For Developers
```bash
# Read these first:
1. ../README.md - Project overview
2. PROJECT_STATUS.md - Current state
3. api_coverage_map.md - API mappings
4. decisions/ - Architecture decisions
```

---

## Configuration

### Required Environment Variables
```bash
FORTIMANAGER_HOST=your-fmg-hostname
FORTIMANAGER_API_KEY=your-api-key
```

### Optional Variables
```bash
FORTIMANAGER_VERIFY_SSL=true
FORTIMANAGER_TIMEOUT=30
LOG_LEVEL=INFO
```

---

## Tool Categories Overview

**Infrastructure (263 tools):**
- Device Management (65)
- Provisioning & Templates (98)
- ADOM Management (27)
- Workspace & Locking (20)
- FMG Operations (40)
- Installation & Updates (16)

**Security & Policy (136 tools):**
- Policy Package Management (50)
- Objects Management (59)
- Security Profiles (27)

**Monitoring & Automation (90 tools):**
- Monitoring & Tasks (58)
- CLI Script Management (12)
- FortiGuard Management (19)
- QoS Management (2)

**Network Services (37 tools):**
- SD-WAN Management (19)
- VPN Management (18)

**Integration (30 tools):**
- Connector Management (11)
- Meta Fields (7)
- CSF (3)
- Sub Fetch (3)
- FMG Cloud (3)
- Docker Management (2)
- DB Cache (2)
- Sys Proxy JSON (2)
- Option Attribute (1)

---

## Common Operations

### Device Management
```python
# List devices
devices = await list_devices(adom="root")

# Add device
result = await add_managed_device(
    device_name="FGT-01",
    device_ip="192.168.1.1",
    username="admin",
    password="password"
)

# Upgrade firmware
await upgrade_device_firmware(
    device_name="FGT-01",
    firmware_version="7.4.2"
)
```

### Policy Management
```python
# List policies
policies = await list_firewall_policies(
    package="default",
    adom="root"
)

# Create policy
await create_firewall_policy(
    package="default",
    policy_data={
        "name": "Allow-Web",
        "srcintf": ["port1"],
        "dstintf": ["port2"],
        "srcaddr": ["internal"],
        "dstaddr": ["all"],
        "service": ["HTTP", "HTTPS"],
        "action": "accept"
    }
)

# Install policies
await install_policy_package(
    package="default",
    devices=["FGT-01"],
    adom="root"
)
```

### Object Management
```python
# Create address
await create_firewall_address(
    name="Web-Server",
    address_type="ipmask",
    subnet="10.0.1.10/32",
    adom="root"
)

# Create service
await create_firewall_service(
    name="Custom-Web",
    tcp_portrange="8080",
    adom="root"
)
```

### Monitoring
```python
# Get system status
status = await get_system_status()

# Monitor task
task_status = await get_task_status(task_id=123)

# Get device health
health = await get_device_health_metrics(
    device_name="FGT-01"
)
```

---

## Best Practices

### Configuration Management
1. Always use workspace locking when making changes
2. Test with install preview before deploying
3. Use metadata for organization
4. Leverage templates for standardization

### Error Handling
1. Check task status for long operations
2. Monitor installation progress
3. Use validation before deployment
4. Keep audit logs

### Performance
1. Use filters to reduce data transfer
2. Batch operations when possible
3. Cache frequently accessed data
4. Monitor system resources

---

## Troubleshooting

### Connection Issues
- Verify `FORTIMANAGER_HOST` is correct
- Check API key permissions
- Confirm SSL certificate if `VERIFY_SSL=true`
- Test network connectivity

### API Errors
- Check FortiManager logs
- Verify ADOM exists
- Confirm object names are unique
- Ensure proper permissions

### Performance
- Review task queue
- Check system resources
- Monitor API response times
- Optimize query filters

---

## Support & Resources

### Documentation
- Project README: `../README.md`
- API Coverage: `api_coverage_map.md`
- Architecture: `architecture.md`
- ADRs: `decisions/`

### External Resources
- FortiManager Documentation
- FastMCP Framework
- MCP Protocol Specification

---

*Last Updated: October 16, 2025 - v1.0.0*


