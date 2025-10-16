#!/bin/bash
# Verification script to check what will be pushed to GitHub

echo "=== Files that will be EXCLUDED from GitHub ==="
echo ""
echo "Checking .gitignore exclusions..."
echo ""

# Check if excluded files exist
if [ -d "FortiManager-7.4.8-JSON-API-Reference" ]; then
    echo "✓ FortiManager-7.4.8-JSON-API-Reference/ - WILL BE EXCLUDED"
else
    echo "  FortiManager-7.4.8-JSON-API-Reference/ - Not present"
fi

if [ -d "FortiManager-how-to-guide" ]; then
    echo "✓ FortiManager-how-to-guide/ - WILL BE EXCLUDED"
else
    echo "  FortiManager-how-to-guide/ - Not present"
fi

if [ -f "fortimanagerapikey.txt" ]; then
    echo "✓ fortimanagerapikey.txt - WILL BE EXCLUDED"
else
    echo "  fortimanagerapikey.txt - Not present"
fi

if [ -d "htmlcov" ]; then
    echo "✓ htmlcov/ - WILL BE EXCLUDED"
else
    echo "  htmlcov/ - Not present"
fi

if [ -d "logs" ]; then
    echo "✓ logs/ - WILL BE EXCLUDED"
else
    echo "  logs/ - Not present"
fi

if [ -f ".env" ]; then
    echo "✓ .env - WILL BE EXCLUDED"
else
    echo "  .env - Not present (good, this should not exist)"
fi

echo ""
echo "=== Files that WILL BE INCLUDED in GitHub ==="
echo ""

# Important files that should be included
files_to_include=(
    "README.md"
    "LICENSE"
    "CHANGELOG.md"
    "TESTING_STATUS.md"
    "RELEASE_CHECKLIST.md"
    "pyproject.toml"
    "Dockerfile"
    "docker-compose.yml"
    "env.example"
    ".gitignore"
    "src/fortimanager_mcp"
    "tests"
    ".notes"
    ".github"
)

for file in "${files_to_include[@]}"; do
    if [ -e "$file" ]; then
        echo "✓ $file"
    else
        echo "✗ $file - MISSING!"
    fi
done

echo ""
echo "=== File Count Summary ==="
echo ""
echo "Python source files:"
find src -name "*.py" 2>/dev/null | wc -l | xargs echo "  "

echo "Documentation files (.notes):"
find .notes -name "*.md" 2>/dev/null | wc -l | xargs echo "  "

echo "Test files:"
find tests -name "*.py" 2>/dev/null | wc -l | xargs echo "  "

echo ""
echo "=== Git Status Check ==="
echo ""

if [ -d ".git" ]; then
    echo "Git repository already initialized"
    git status --short 2>/dev/null || echo "Run 'git status' to see current state"
else
    echo "Git repository not yet initialized"
    echo "Run: git init"
fi

echo ""
echo "=== Next Steps ==="
echo ""
echo "1. Authenticate with GitHub CLI:"
echo "   gh auth login"
echo ""
echo "2. Initialize and push repository:"
echo "   See GITHUB_SETUP_GUIDE.md for detailed instructions"
echo ""
echo "3. Verify nothing sensitive is included:"
echo "   git add --dry-run . | grep -E '(apikey|token|password|secret|.env$)'"
echo ""

