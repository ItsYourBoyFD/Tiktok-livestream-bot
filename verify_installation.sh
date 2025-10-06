#!/bin/bash
# Installation Verification Script for TikTok Bot

set -e

echo "🔍 TikTok Bot - Installation Verification"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check counter
CHECKS_PASSED=0
CHECKS_FAILED=0

check_pass() {
    echo -e "${GREEN}✓${NC} $1"
    ((CHECKS_PASSED++))
}

check_fail() {
    echo -e "${RED}✗${NC} $1"
    ((CHECKS_FAILED++))
}

check_warn() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Check Python
echo "📋 Checking Requirements..."
echo ""

if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    check_pass "Python 3 installed (version $PYTHON_VERSION)"
else
    check_fail "Python 3 not found"
fi

# Check pip
if command -v pip &> /dev/null || command -v pip3 &> /dev/null; then
    check_pass "pip installed"
else
    check_fail "pip not found"
fi

# Check Docker (optional)
if command -v docker &> /dev/null; then
    check_pass "Docker installed (optional)"
else
    check_warn "Docker not installed (optional, but recommended for production)"
fi

echo ""
echo "📁 Checking Project Files..."
echo ""

# Check required files
FILES=("main.py" "utils.py" "web_app.py" "requirements.txt" "templates/index.html" "static/css/style.css" "static/js/app.js")

for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        check_pass "$file exists"
    else
        check_fail "$file missing"
    fi
done

# Check Data directory
if [ -d "Data" ]; then
    check_pass "Data directory exists"
    
    if [ -f "Data/Proxies.txt" ]; then
        PROXY_COUNT=$(wc -l < Data/Proxies.txt | tr -d ' ')
        if [ "$PROXY_COUNT" -gt 0 ]; then
            check_pass "Proxies file exists with $PROXY_COUNT proxies"
        else
            check_warn "Proxies file is empty - add proxies before running"
        fi
    else
        check_warn "Proxies.txt not found - will be created on first run"
    fi
else
    check_fail "Data directory missing"
fi

echo ""
echo "🐍 Checking Python Syntax..."
echo ""

# Check Python files syntax
for py_file in main.py utils.py web_app.py; do
    if python3 -m py_compile "$py_file" 2>/dev/null; then
        check_pass "$py_file syntax valid"
    else
        check_fail "$py_file has syntax errors"
    fi
done

echo ""
echo "📦 Checking Dependencies..."
echo ""

# Try to import key modules
MODULES=("flask" "requests" "flask_socketio")

for module in "${MODULES[@]}"; do
    if python3 -c "import $module" 2>/dev/null; then
        check_pass "$module installed"
    else
        check_warn "$module not installed - run: pip install -r requirements.txt"
    fi
done

echo ""
echo "🔧 Checking Deployment Files..."
echo ""

DEPLOY_FILES=("Dockerfile" "docker-compose.yml" "gunicorn_config.py" "nginx.conf" "start.sh")

for file in "${DEPLOY_FILES[@]}"; do
    if [ -f "$file" ]; then
        check_pass "$file exists"
    else
        check_fail "$file missing"
    fi
done

# Check if start.sh is executable
if [ -x "start.sh" ]; then
    check_pass "start.sh is executable"
else
    check_warn "start.sh not executable - run: chmod +x start.sh"
fi

echo ""
echo "=========================================="
echo "📊 Verification Summary"
echo "=========================================="
echo ""
echo -e "Checks Passed: ${GREEN}$CHECKS_PASSED${NC}"
echo -e "Checks Failed: ${RED}$CHECKS_FAILED${NC}"
echo ""

if [ $CHECKS_FAILED -eq 0 ]; then
    echo -e "${GREEN}✅ All critical checks passed!${NC}"
    echo ""
    echo "🚀 Ready to start!"
    echo ""
    echo "Quick Start:"
    echo "  1. Add proxies to Data/Proxies.txt"
    echo "  2. Run: ./start.sh"
    echo "  3. Open: http://localhost:5000"
    echo ""
else
    echo -e "${RED}❌ Some checks failed. Please fix the issues above.${NC}"
    echo ""
fi

echo "📚 Documentation:"
echo "  - QUICK_START.md - Getting started guide"
echo "  - WEB_INTERFACE_GUIDE.md - API documentation"
echo "  - DEPLOYMENT.md - Production deployment"
echo ""
echo "💬 Support: discord.gg/devcenter"
echo ""
