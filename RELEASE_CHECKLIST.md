# Release Checklist

Pre-release verification checklist for FortiManager MCP Server.

---

## Version 0.1.0-beta - October 16, 2025

### Code Quality
- [x] Zero linter errors (ruff)
- [x] Zero type errors (mypy)
- [x] All imports resolve correctly
- [x] PEP 8 compliance verified
- [x] 100% type hint coverage

### Build & Deployment
- [x] Docker build completes successfully
- [x] Docker container runs without errors
- [x] All dependencies resolve correctly
- [x] Virtual environment creation works
- [x] Package installation completes

### Documentation
- [x] README.md updated with beta disclaimer
- [x] Version updated to 0.1.0-beta
- [x] CHANGELOG.md created
- [x] TESTING_STATUS.md created
- [x] All documentation reviewed for accuracy
- [x] API coverage map is accurate
- [x] No outdated statistics in docs
- [x] Professional tone throughout

### Project Configuration
- [x] pyproject.toml version updated
- [x] Dependencies listed correctly
- [x] Build configuration verified
- [x] Test configuration present
- [x] Linter configuration correct

### Security
- [x] No credentials in repository
- [x] .gitignore configured properly
- [x] env.example provided
- [x] Security best practices documented
- [x] API token usage documented

### Testing
- [x] Non-intrusive test framework in place
- [x] Integration test structure exists
- [x] Testing documentation complete
- [x] Testing status clearly communicated

### GitHub Preparation
- [x] .gitignore includes appropriate files
- [ ] LICENSE file present (to be added)
- [x] README.md professional and accurate
- [x] CHANGELOG.md follows standard format
- [x] Contributing guidelines (in README)
- [x] Beta status clearly marked

### Beta Release Specific
- [x] Beta disclaimer in README
- [x] Testing status documented
- [x] Known limitations listed
- [x] Production testing roadmap defined
- [x] Community testing encouraged
- [x] Issue reporting process documented

---

## Pre-Release Tasks

### Required Before Release
1. [x] Code quality verification
2. [x] Docker build test
3. [x] Documentation review
4. [x] Version numbering
5. [x] Beta disclaimers added
6. [ ] LICENSE file (needs decision)
7. [ ] GitHub repository initialized
8. [ ] Release notes prepared

### Recommended Before Release
1. [x] TESTING_STATUS.md created
2. [x] RELEASE_CHECKLIST.md created
3. [x] CHANGELOG.md created
4. [ ] GitHub Issues templates
5. [ ] Pull request template
6. [ ] Contributing guide (basic in README)
7. [ ] Code of conduct (optional for beta)

### Post-Release Tasks
1. [ ] Create GitHub release v0.1.0-beta
2. [ ] Tag release in git
3. [ ] Announce in relevant communities
4. [ ] Monitor for issues
5. [ ] Respond to community feedback
6. [ ] Begin comprehensive testing program

---

## License Decision Required

**Current Status:** No LICENSE file present

**Options:**
1. **MIT License** - Permissive, widely used
2. **Apache 2.0** - Permissive with patent grant
3. **GPL v3** - Copyleft, requires derivatives to be open source
4. **Proprietary** - Custom terms

**Recommendation:** MIT or Apache 2.0 for open source project

---

## GitHub Repository Setup

### Repository Settings
- [ ] Repository name: `fortimanager-mcp`
- [ ] Description: "Model Context Protocol server for FortiManager - Beta"
- [ ] Topics: `fortimanager`, `mcp`, `fortinet`, `api`, `automation`
- [ ] Website: (optional)
- [ ] Issues enabled
- [ ] Projects disabled (optional)
- [ ] Wiki disabled (optional)
- [ ] Discussions enabled (optional)

### Branch Protection
- [ ] Protect main branch
- [ ] Require pull request reviews
- [ ] Require status checks
- [ ] No force push
- [ ] No deletion

### Labels
- [ ] `bug` - Something isn't working
- [ ] `enhancement` - New feature or request
- [ ] `documentation` - Documentation improvements
- [ ] `testing` - Testing related
- [ ] `beta-feedback` - Feedback from beta users
- [ ] `help wanted` - Extra attention needed
- [ ] `good first issue` - Good for newcomers

---

## Release Notes Template

```markdown
# FortiManager MCP Server v0.1.0-beta

## Beta Release

This is the initial beta release of the FortiManager MCP Server, providing complete coverage of all documented FortiManager 7.4.8 JSON-RPC API operations.

### What's Included

- 590 MCP tools covering 100% of documented API operations
- Complete device management (116 operations)
- Complete provisioning & templates (82 operations)
- Complete policy management (77 operations)
- Complete object management (61 operations)
- Complete ADOM management (36 operations)
- Complete security profiles (35 operations)
- Full system operations (30 operations)
- And 13 additional operation categories

### Beta Status

**Important:** While approximately 200 tools have been tested in production environments, comprehensive testing of all 590 tools is ongoing. This beta release is suitable for:

- Development and testing environments
- Proof of concept deployments
- Community testing and feedback
- Non-critical automation tasks

**Not recommended for:** Business-critical production deployments without thorough testing.

### Getting Started

See [README.md](README.md) for installation and configuration instructions.

### Testing & Feedback

We encourage the community to test the tools and report issues. See [TESTING_STATUS.md](TESTING_STATUS.md) for testing guidelines.

### Known Limitations

- Not all tools have been tested in production
- Tested primarily against FortiManager 7.4.8
- Some advanced operations may require validation

### Next Steps

- Comprehensive production testing of all tools
- Community feedback incorporation
- Bug fixes and improvements
- Move toward 1.0.0 stable release

### Contributing

Contributions are welcome! Please see the README for guidelines.
```

---

## Verification Commands

```bash
# Build verification
docker build -t fortimanager-mcp:test .

# Linter check
ruff check src/

# Type check
mypy src/

# Package build
uv build

# Test import
python -c "import fortimanager_mcp"
```

---

## Final Checks Before Publishing

- [ ] All checkboxes above marked
- [ ] Version numbers consistent everywhere
- [ ] Docker build tested
- [ ] Documentation reviewed
- [ ] Beta disclaimers present
- [ ] Testing status documented
- [ ] License decided and added
- [ ] Release notes prepared
- [ ] GitHub repository ready

---

*Checklist last updated: October 16, 2025*

