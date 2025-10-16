# Documentation Directory

This directory contains comprehensive technical documentation for the FortiManager MCP Server project.

## Quick Navigation

### Getting Started
Start with these documents to understand the project:

1. [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Quick start guide and common operations
2. [PROJECT_STATUS.md](PROJECT_STATUS.md) - Current project status and capabilities
3. [_INDEX.md](_INDEX.md) - Complete documentation index

### Technical Reference
Detailed technical information:

4. [api_coverage_map.md](api_coverage_map.md) - API coverage analysis by category
5. [architecture.md](architecture.md) - System architecture and design patterns
6. [directory_structure.md](directory_structure.md) - Codebase organization

### Development Documentation
Historical and planning information:

7. [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) - Development overview
8. [DEVELOPMENT_HISTORY.md](DEVELOPMENT_HISTORY.md) - Version timeline
9. [implementation_plan_full_coverage.md](implementation_plan_full_coverage.md) - Historical roadmap
10. [decisions/](decisions/) - Architecture Decision Records (ADRs)

## Documentation Organization

```
.notes/
├── README.md (this file)
├── _INDEX.md
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

## Key Statistics

**Current Version:** 1.0.0  
**Total MCP Tools:** 590  
**API Coverage:** 100% (555/555 operations)  
**Code Quality:** Zero linter errors  
**Type Coverage:** 100%

## Documentation Guidelines

### For New Contributors
1. Read QUICK_REFERENCE.md for setup
2. Review PROJECT_STATUS.md for capabilities
3. Check architecture.md for system design
4. Consult ADRs for design decisions

### For Developers
1. Update api_coverage_map.md when adding tools
2. Create ADRs for architectural changes
3. Update PROJECT_STATUS.md for major features
4. Add examples to QUICK_REFERENCE.md

### Documentation Standards
- Keep information accurate and up-to-date
- Use clear, professional language
- Include code examples where helpful
- Cross-reference related documents
- Date significant updates

## Maintenance

Last comprehensive review: October 16, 2025

Regular maintenance includes:
- Accuracy verification
- Stats updates
- Link validation
- Format consistency
- Obsolete content removal

---

For questions about documentation, see [_INDEX.md](_INDEX.md) for detailed navigation help.
