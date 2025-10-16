# GitHub Setup Guide

This guide will help you clean your existing GitHub repository and push the FortiManager MCP Server project.

---

## Step 1: Authenticate with GitHub CLI

```bash
gh auth login
```

Follow the prompts:
- Choose: `GitHub.com`
- Choose: `HTTPS` (recommended)
- Authenticate: `Y` (yes)
- Choose: `Login with a web browser`
- Copy the one-time code and press Enter
- Complete authentication in your browser

Verify authentication:
```bash
gh auth status
```

---

## Step 2: Clean the Existing Repository

⚠️ **Warning:** This will delete all content in your existing `fortimanager-mcp` repository!

### Option A: Clean via GitHub CLI (Recommended)

```bash
# Navigate to the project directory
cd /Users/jamievanderpijll/fortimanager-mcp

# View current repo (if already connected)
gh repo view jmpijll/fortimanager-mcp

# The repo exists but we'll overwrite it with a fresh push
```

### Option B: Clean via GitHub Web Interface

1. Go to https://github.com/jmpijll/fortimanager-mcp
2. Click "Settings"
3. Scroll to "Danger Zone"
4. Click "Delete this repository"
5. Type the repository name to confirm
6. Click "I understand the consequences, delete this repository"

Then create a new empty repository:
```bash
gh repo create jmpijll/fortimanager-mcp --public --description "Model Context Protocol server for FortiManager - Beta"
```

---

## Step 3: Initialize Local Git Repository

```bash
cd /Users/jamievanderpijll/fortimanager-mcp

# Initialize git (if not already initialized)
git init

# Add the GitHub remote
git remote add origin https://github.com/jmpijll/fortimanager-mcp.git

# Or if remote already exists, update it
git remote set-url origin https://github.com/jmpijll/fortimanager-mcp.git
```

---

## Step 4: Verify Files to Exclude

Check what will be committed (should NOT include):
- ❌ `FortiManager-7.4.8-JSON-API-Reference/`
- ❌ `FortiManager-how-to-guide/`
- ❌ `fortimanagerapikey.txt`
- ❌ `htmlcov/`
- ❌ `logs/`
- ❌ `__pycache__/`
- ❌ `.env`

Check what will be included:
```bash
git status

# Or see what would be added
git add --dry-run .
```

---

## Step 5: Create Initial Commit

```bash
# Add all files (respecting .gitignore)
git add .

# Verify what's staged
git status

# Create initial commit
git commit -m "Initial commit - FortiManager MCP Server v0.1.0-beta

- 590 MCP tools covering 100% of FortiManager 7.4.8 API operations
- Complete documentation and testing roadmap
- Docker deployment ready
- Beta release with ~34% tools production-tested
"

# Push to GitHub
git branch -M main
git push -u origin main --force
```

Note: Using `--force` because we're completely replacing the old repository content.

---

## Step 6: Create GitHub Release

```bash
# Create a new release
gh release create v0.1.0-beta \
  --title "FortiManager MCP Server v0.1.0-beta - Initial Beta Release" \
  --notes-file RELEASE_NOTES.md \
  --prerelease
```

Or create manually via web interface:
1. Go to https://github.com/jmpijll/fortimanager-mcp/releases
2. Click "Draft a new release"
3. Tag: `v0.1.0-beta`
4. Title: `FortiManager MCP Server v0.1.0-beta - Initial Beta Release`
5. Copy content from `PRE_RELEASE_SUMMARY.md` GitHub Release Template section
6. Check "This is a pre-release"
7. Click "Publish release"

---

## Step 7: Configure Repository Settings

```bash
# Enable issues and set description
gh repo edit jmpijll/fortimanager-mcp \
  --description "Model Context Protocol server for FortiManager JSON-RPC API - Beta Release" \
  --enable-issues \
  --enable-wiki=false

# Add topics
gh repo edit jmpijll/fortimanager-mcp \
  --add-topic fortimanager \
  --add-topic mcp \
  --add-topic fortinet \
  --add-topic api \
  --add-topic automation \
  --add-topic python \
  --add-topic docker \
  --add-topic beta
```

---

## Step 8: Set Up Branch Protection (Optional)

```bash
# Protect main branch
gh api repos/jmpijll/fortimanager-mcp/branches/main/protection \
  -X PUT \
  -f required_status_checks='null' \
  -f enforce_admins=true \
  -f required_pull_request_reviews='null' \
  -f restrictions='null'
```

Or configure via web interface:
1. Go to Settings → Branches
2. Add rule for `main` branch
3. Enable desired protections

---

## Step 9: Verify Everything

```bash
# View repository
gh repo view jmpijll/fortimanager-mcp --web

# Check if files are correct
# Should NOT see:
# - FortiManager API documentation folders
# - API key files
# - htmlcov/
# - logs/

# Should see:
# - README.md with beta disclaimer
# - LICENSE (MIT)
# - All source code
# - Documentation (.notes/)
# - Docker files
# - GitHub Actions workflows
```

---

## Files That Will Be Pushed

### Root Directory
- ✅ README.md
- ✅ LICENSE
- ✅ CHANGELOG.md
- ✅ TESTING_STATUS.md
- ✅ RELEASE_CHECKLIST.md
- ✅ PRE_RELEASE_SUMMARY.md
- ✅ pyproject.toml
- ✅ Dockerfile
- ✅ docker-compose.yml
- ✅ env.example
- ✅ .gitignore

### Source Code
- ✅ src/fortimanager_mcp/ (all Python modules)

### Tests
- ✅ tests/ (integration tests)

### Documentation
- ✅ .notes/ (technical documentation)

### GitHub
- ✅ .github/workflows/ (CI/CD)
- ✅ .github/ISSUE_TEMPLATE/ (issue templates)

---

## Troubleshooting

### Authentication Issues
```bash
# Re-authenticate
gh auth logout
gh auth login
```

### Push Rejected
```bash
# Force push (since we're replacing old content)
git push -u origin main --force
```

### Remote Already Exists
```bash
# Remove old remote
git remote remove origin

# Add new remote
git remote add origin https://github.com/jmpijll/fortimanager-mcp.git
```

### Files Accidentally Committed
```bash
# Remove from git but keep locally
git rm --cached FortiManager-7.4.8-JSON-API-Reference/ -r
git rm --cached fortimanagerapikey.txt

# Commit the removal
git commit -m "Remove files that shouldn't be in public repo"
git push
```

---

## Post-Push Checklist

After pushing to GitHub:

- [ ] Verify repository is accessible: https://github.com/jmpijll/fortimanager-mcp
- [ ] Check no API documentation is visible
- [ ] Check no API keys are visible
- [ ] Verify README displays correctly
- [ ] Verify LICENSE is present
- [ ] Check GitHub Actions are running
- [ ] Create v0.1.0-beta release
- [ ] Add repository description and topics
- [ ] Enable Issues
- [ ] Announce release (optional)

---

## Next Steps

1. Monitor GitHub Issues for bug reports
2. Respond to community feedback
3. Begin systematic testing of remaining tools
4. Document test results in TESTING_STATUS.md
5. Plan next beta release (0.2.0-beta)

---

*Setup guide created: October 16, 2025*

