# Quick Push Commands

Copy and paste these commands in order to push to GitHub.

---

## Step 1: Authenticate with GitHub CLI

```bash
gh auth login
```

Choose:
- GitHub.com
- HTTPS
- Yes (authenticate)
- Login with web browser
- Complete authentication in browser

Verify:
```bash
gh auth status
```

---

## Step 2: Clean & Prepare Repository (if needed)

If your existing repo has content you want to replace:

### Option A: Delete and recreate (cleanest)
```bash
# Delete the old repository (CAREFUL!)
gh repo delete jmpijll/fortimanager-mcp --yes

# Create fresh empty repository
gh repo create jmpijll/fortimanager-mcp --public \
  --description "Model Context Protocol server for FortiManager JSON-RPC API - Beta Release" \
  --clone=false
```

### Option B: Keep and force push over it
Just continue to Step 3 and use `--force` flag when pushing.

---

## Step 3: Initialize Local Git

```bash
cd /Users/jamievanderpijll/fortimanager-mcp

# Initialize git
git init

# Add remote
git remote add origin https://github.com/jmpijll/fortimanager-mcp.git

# Or if remote exists, update it
git remote set-url origin https://github.com/jmpijll/fortimanager-mcp.git
```

---

## Step 4: Verify Files (Safety Check)

```bash
# Run verification script
./verify_files.sh

# Check what will be added (dry run)
git add --dry-run .

# Look for anything suspicious (should return nothing)
git add --dry-run . | grep -E '(apikey|token|password|secret|\.env$|how-to-guide|API-Reference)'
```

If you see any API keys or documentation folders, STOP and check .gitignore.

---

## Step 5: Commit and Push

```bash
# Add all files (respecting .gitignore)
git add .

# Check status
git status

# Create initial commit
git commit -m "Initial commit - FortiManager MCP Server v0.1.0-beta

- 590 MCP tools covering 100% of FortiManager 7.4.8 API operations
- Complete documentation and testing roadmap
- Docker deployment ready
- Beta release with ~34% tools production-tested
- MIT License
- GitHub Actions for CI/CD
"

# Set main branch and push
git branch -M main
git push -u origin main --force
```

Note: `--force` is needed because we're replacing old content.

---

## Step 6: Configure Repository

```bash
# Set description and topics
gh repo edit jmpijll/fortimanager-mcp \
  --description "Model Context Protocol server for FortiManager JSON-RPC API - Beta Release" \
  --enable-issues \
  --enable-wiki=false

# Add topics for discoverability
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

## Step 7: Create GitHub Release

```bash
# Create beta release
gh release create v0.1.0-beta \
  --title "FortiManager MCP Server v0.1.0-beta - Initial Beta Release" \
  --notes "## Beta Release - Complete API Coverage

This is the initial beta release providing complete coverage of all documented FortiManager 7.4.8 JSON-RPC API operations.

### Highlights
- **590 MCP tools** covering **100% of documented operations**
- **Zero linter errors** and **100% type safety**
- **Docker deployment ready**
- **Comprehensive documentation**

### Beta Status ⚠️
While approximately 200 tools have been tested in production environments, comprehensive testing of all 590 tools is ongoing.

**Please test thoroughly in non-production environments before production use.**

### Quick Start
\`\`\`bash
docker run -e FORTIMANAGER_HOST=<host> \\
           -e FORTIMANAGER_API_TOKEN=<token> \\
           jmpijll/fortimanager-mcp:0.1.0-beta
\`\`\`

### Documentation
- [README.md](README.md) - Getting started
- [TESTING_STATUS.md](TESTING_STATUS.md) - Testing roadmap
- [CHANGELOG.md](CHANGELOG.md) - Version history

### Contributing
Community contributions welcome! Report issues, share test results, and provide feedback.

See [TESTING_STATUS.md](TESTING_STATUS.md) for testing guidelines." \
  --prerelease
```

---

## Step 8: Verify Repository

```bash
# Open repository in browser
gh repo view jmpijll/fortimanager-mcp --web

# Check that these are NOT visible:
# ❌ FortiManager-7.4.8-JSON-API-Reference/
# ❌ FortiManager-how-to-guide/
# ❌ fortimanagerapikey.txt
# ❌ htmlcov/
# ❌ logs/
# ❌ .env files

# Check that these ARE visible:
# ✓ README.md
# ✓ LICENSE
# ✓ src/
# ✓ .github/
# ✓ Documentation files
```

---

## Troubleshooting

### Authentication Failed
```bash
gh auth logout
gh auth login
```

### Remote Already Exists Error
```bash
git remote remove origin
git remote add origin https://github.com/jmpijll/fortimanager-mcp.git
```

### Push Rejected
```bash
# Force push (we're replacing old content)
git push -u origin main --force
```

### Accidental File Committed
```bash
# Remove from git but keep locally
git rm --cached <filename>
git commit -m "Remove sensitive file"
git push
```

---

## All-in-One Script (Advanced)

**WARNING**: This will delete your existing repo and replace it. Make sure you're ready!

```bash
#!/bin/bash
set -e

echo "🚀 Pushing FortiManager MCP Server to GitHub"
echo ""

# Verify we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: Not in fortimanager-mcp directory"
    exit 1
fi

# Check authentication
echo "📝 Checking GitHub authentication..."
if ! gh auth status &>/dev/null; then
    echo "❌ Not authenticated. Run: gh auth login"
    exit 1
fi

# Safety check
echo "⚠️  This will DELETE your existing repository and push fresh code."
echo "Press Ctrl+C to cancel, or Enter to continue..."
read

# Delete old repo
echo "🗑️  Deleting old repository..."
gh repo delete jmpijll/fortimanager-mcp --yes || echo "Repo didn't exist or couldn't delete"

# Create new repo
echo "📦 Creating new repository..."
gh repo create jmpijll/fortimanager-mcp --public \
  --description "Model Context Protocol server for FortiManager JSON-RPC API - Beta Release" \
  --clone=false

# Initialize git
echo "🔧 Initializing git..."
git init
git remote add origin https://github.com/jmpijll/fortimanager-mcp.git || git remote set-url origin https://github.com/jmpijll/fortimanager-mcp.git

# Add and commit
echo "📝 Creating commit..."
git add .
git commit -m "Initial commit - FortiManager MCP Server v0.1.0-beta

- 590 MCP tools covering 100% of FortiManager 7.4.8 API operations
- Complete documentation and testing roadmap
- Docker deployment ready
- Beta release with ~34% tools production-tested
- MIT License
- GitHub Actions for CI/CD
"

# Push
echo "🚀 Pushing to GitHub..."
git branch -M main
git push -u origin main --force

# Configure repo
echo "⚙️  Configuring repository..."
gh repo edit jmpijll/fortimanager-mcp \
  --description "Model Context Protocol server for FortiManager JSON-RPC API - Beta Release" \
  --enable-issues \
  --enable-wiki=false

gh repo edit jmpijll/fortimanager-mcp \
  --add-topic fortimanager \
  --add-topic mcp \
  --add-topic fortinet \
  --add-topic api \
  --add-topic automation \
  --add-topic python \
  --add-topic docker \
  --add-topic beta

echo ""
echo "✅ Successfully pushed to GitHub!"
echo ""
echo "🌐 View your repository:"
gh repo view jmpijll/fortimanager-mcp --web
```

Save this as `push_to_github.sh` and run:
```bash
chmod +x push_to_github.sh
./push_to_github.sh
```

---

*Ready to push: October 16, 2025*

