# Documentation Index

This directory contains technical documentation for the FortiManager MCP Server project.

---

## Quick Navigation

### Getting Started
1. **README.md** - Documentation directory overview
2. **QUICK_REFERENCE.md** - Quick start and common operations
3. **PROJECT_STATUS.md** - Current capabilities and status

### Technical Documentation
4. **api_coverage_map.md** - API coverage by category
5. **architecture.md** - System architecture and design
6. **directory_structure.md** - Codebase organization
7. **IMPLEMENTATION_SUMMARY.md** - Development overview

### Historical Records
8. **DEVELOPMENT_HISTORY.md** - Version timeline
9. **implementation_plan_full_coverage.md** - Planning archive
10. **decisions/** - Architecture Decision Records

---

## Document Descriptions

### README.md
Overview of the documentation structure and navigation guide.

### QUICK_REFERENCE.md
- Quick start commands
- Common operation examples
- Configuration reference
- Troubleshooting guide

### PROJECT_STATUS.md
- Current metrics and capabilities
- Coverage by category
- Module structure
- Integration guidance

### api_coverage_map.md
- Detailed coverage breakdown
- Tools per category
- Implementation status
- Operation mapping

### architecture.md
- System design principles
- Component architecture
- API client patterns
- Tool layer design

### directory_structure.md
- Codebase organization
- Module descriptions
- File naming conventions

### IMPLEMENTATION_SUMMARY.md
- Development overview
- Coverage statistics
- Technical implementation
- Quality metrics

### DEVELOPMENT_HISTORY.md
- Version history
- Major milestones
- Technical decisions

### implementation_plan_full_coverage.md
- Historical planning document
- Phase roadmap
- Coverage targets

### decisions/
Architecture Decision Records documenting key technical choices:
- ADR-001: Python with FastMCP framework
- ADR-002: Token-based authentication
- ADR-003: Streamable HTTP client
- ADR-004: Integration testing approach
- ADR-005: Tool categorization strategy

---

## Finding Information

**Get started quickly:**  
→ QUICK_REFERENCE.md

**Understand capabilities:**  
→ PROJECT_STATUS.md, api_coverage_map.md

**Learn architecture:**  
→ architecture.md, directory_structure.md

**Review development:**  
→ IMPLEMENTATION_SUMMARY.md, DEVELOPMENT_HISTORY.md

**Understand decisions:**  
→ decisions/ADR-*.md

---

## Project Statistics (v1.0.0)

- **Total MCP Tools:** 590
- **API Coverage:** 100% (555/555 operations)
- **Complete Categories:** 19/24 at 100%
- **Code Quality:** Zero linter errors
- **Type Coverage:** 100%
- **Documentation:** Comprehensive on all tools

---

## Documentation Structure

```
.notes/
├── _INDEX.md (this file)
├── README.md
├── QUICK_REFERENCE.md
├── PROJECT_STATUS.md
├── IMPLEMENTATION_SUMMARY.md
├── DEVELOPMENT_HISTORY.md
├── api_coverage_map.md
├── architecture.md
├── directory_structure.md
├── implementation_plan_full_coverage.md
└── decisions/
    ├── ADR-001-python-fastmcp.md
    ├── ADR-002-token-auth.md
    ├── ADR-003-streamable-http.md
    ├── ADR-004-integration-testing.md
    └── ADR-005-tool-categorization.md
```

---

## Maintenance Guidelines

When updating the codebase:

1. Update PROJECT_STATUS.md for capability changes
2. Update api_coverage_map.md for new tools
3. Add ADRs for architectural decisions
4. Update DEVELOPMENT_HISTORY.md for milestones
5. Update QUICK_REFERENCE.md for new operations

---

*Last Updated: October 16, 2025*  
*Documentation Version: 1.0.0*
