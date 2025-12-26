#!/bin/bash
# Chimera Browser Provider Test Runner
# Tests all free web chatbot providers

set -e

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║     CHIMERA BROWSER PROVIDER TEST SUITE                     ║"
echo "║     Testing FREE Web Chatbot → API Conversion               ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Check if server is running
echo "🔍 Checking if Chimera server is running..."
if ! curl -s http://localhost:8000/api/status > /dev/null 2>&1; then
    echo "❌ ERROR: Chimera server is not running!"
    echo ""
    echo "Please start the server first:"
    echo "  Terminal 1: make dev"
    echo "  Terminal 2: ./scripts/test_browser_providers.sh"
    echo ""
    exit 1
fi

echo "✓ Server is running"
echo ""

# Display instructions
echo "📋 BEFORE RUNNING TESTS:"
echo ""
echo "1. Open Command Center: http://localhost:5173"
echo "2. Click 'Spawn' next to each provider you want to test"
echo "3. Log in manually in the browser windows"
echo "4. Minimize browsers (don't close!)"
echo ""
echo "Press ENTER when ready, or Ctrl+C to cancel..."
read

echo ""
echo "🧪 Running Browser Provider Tests..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Run tests with verbose output
uv run pytest tests/test_browser_providers.py -v -s -m browser \
    || { echo ""; echo "❌ Some tests failed. Check output above."; exit 1; }

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Browser Provider Tests Complete!"
echo ""
echo "📊 To run session tests:"
echo "   uv run pytest tests/test_browser_sessions.py -v -s -m browser"
echo ""
echo "📊 To run all tests:"
echo "   uv run pytest -v"
echo ""
