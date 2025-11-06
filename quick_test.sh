#!/bin/bash
echo "🚀 Quick AI Features Test"

# Check server
echo "📡 Testing server connection..."
curl -s http://127.0.0.1:8000/api/notes/ | head -c 100

# Test analytics
echo -e "\n📊 Testing analytics..."
curl -s http://127.0.0.1:8000/api/analytics/ | jq '.analytics // "No data"'

# Test languages
echo -e "\n🌍 Testing languages..."
curl -s http://127.0.0.1:8000/api/languages/ | jq '.languages | keys'

# Test dashboard
echo -e "\n📈 Testing dashboard..."
curl -s http://127.0.0.1:8000/api/dashboard/ | jq '.dashboard // "No data"'

echo -e "\n✅ Quick test complete!"