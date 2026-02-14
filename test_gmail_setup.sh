#!/bin/bash
echo "=== Gmail Watcher Setup Check ==="
echo ""
echo "1. Checking credentials.json..."
if [ -f "credentials.json" ]; then
    echo "   ✅ Found"
else
    echo "   ❌ Missing - Download from Google Cloud Console"
fi
echo ""
echo "2. Checking token.json..."
if [ -f "token.json" ]; then
    echo "   ✅ Found (already authenticated)"
else
    echo "   ⏳ Not found (will be created on first run)"
fi
echo ""
echo "3. Checking logs directory..."
if [ -d "logs" ]; then
    echo "   ✅ Ready"
else
    echo "   ❌ Missing"
fi
echo ""
echo "4. Checking gmail_watcher.py..."
if [ -f "AI_Employee_Vault/scripts/gmail_watcher.py" ]; then
    echo "   ✅ Ready"
else
    echo "   ❌ Missing"
fi
echo ""
echo "=== Next Steps ==="
if [ ! -f "credentials.json" ]; then
    echo "📋 Get credentials.json from: https://console.cloud.google.com/"
    echo "   1. Enable Gmail API"
    echo "   2. Create OAuth Desktop credentials"
    echo "   3. Download and save as credentials.json"
else
    echo "🚀 Ready to run!"
    echo "   Run: AI_Employee_Vault/venv/Scripts/python.exe AI_Employee_Vault/scripts/gmail_watcher.py"
fi
