#!/bin/bash

# WhatsApp Education Bot - Complete Integration Test Script
# This script tests both n8n and Flask endpoints

echo "🧪 WhatsApp Education Bot Integration Tests"
echo "=========================================="

# Test Variables
N8N_URL="https://06945024e292.ngrok-free.app/webhook/n8n-whatsapp-webhook"
FLASK_URL="http://localhost:5001/whatsapp"
TEST_DATA="Body=hi&From=whatsapp:+1234567890&To=whatsapp:+0987654321"

echo ""
echo "📋 Test Configuration:"
echo "  n8n Webhook: $N8N_URL"
echo "  Flask Backup: $FLASK_URL"
echo "  Test Message: 'hi' from +1234567890"
echo ""

# Test 1: n8n Webhook
echo "🔍 Test 1: n8n Webhook Endpoint"
echo "--------------------------------"
response=$(curl -s -w "HTTP_CODE:%{http_code}" -X POST "$N8N_URL" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "$TEST_DATA")

http_code=$(echo "$response" | sed -n 's/.*HTTP_CODE:\([0-9]*\)$/\1/p')
body=$(echo "$response" | sed 's/HTTP_CODE:[0-9]*$//')

echo "HTTP Status: $http_code"
if [ -n "$body" ] && [[ "$body" == *"<Response>"* ]]; then
    echo "✅ n8n Response: TwiML detected"
    echo "   Content: $(echo "$body" | head -c 100)..."
else
    echo "❌ n8n Response: Empty or invalid"
    echo "   Body: $body"
fi
echo ""

# Test 2: Flask Backup
echo "🔍 Test 2: Flask Backup Endpoint"
echo "--------------------------------"
response=$(curl -s -w "HTTP_CODE:%{http_code}" -X POST "$FLASK_URL" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "$TEST_DATA")

http_code=$(echo "$response" | sed -n 's/.*HTTP_CODE:\([0-9]*\)$/\1/p')
body=$(echo "$response" | sed 's/HTTP_CODE:[0-9]*$//')

echo "HTTP Status: $http_code"
if [ -n "$body" ] && [[ "$body" == *"<Response>"* ]]; then
    echo "✅ Flask Response: TwiML detected"
    echo "   Content: $(echo "$body" | head -c 100)..."
else
    echo "❌ Flask Response: Empty or invalid"
    echo "   Body: $body"
fi
echo ""

# Test 3: Service Health Check
echo "🔍 Test 3: Service Health Check"
echo "-------------------------------"

# Check n8n
if curl -s http://localhost:5678/ > /dev/null; then
    echo "✅ n8n Service: Running on port 5678"
else
    echo "❌ n8n Service: Not accessible"
fi

# Check Flask
if curl -s http://localhost:5001/ > /dev/null; then
    echo "✅ Flask Service: Running on port 5001"
else
    echo "❌ Flask Service: Not accessible"
fi

# Check ngrok
if curl -s http://localhost:4040/api/tunnels > /dev/null; then
    echo "✅ ngrok Tunnel: Active"
    ngrok_url=$(curl -s http://localhost:4040/api/tunnels | grep -o '"public_url":"[^"]*' | cut -d'"' -f4 | grep https)
    echo "   URL: $ngrok_url"
else
    echo "❌ ngrok Tunnel: Not accessible"
fi
echo ""

# Test 4: Advanced Message Tests
echo "🔍 Test 4: Advanced Message Tests"
echo "---------------------------------"

# Test FAQ
echo "Testing FAQ query..."
faq_response=$(curl -s -X POST "$FLASK_URL" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "Body=fees&From=whatsapp:+1234567890&To=whatsapp:+0987654321")

if [[ "$faq_response" == *"Fee Structure"* ]]; then
    echo "✅ FAQ Test: Working"
else
    echo "❌ FAQ Test: Failed"
fi

# Test Resources
echo "Testing Resources query..."
resource_response=$(curl -s -X POST "$FLASK_URL" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "Body=notes&From=whatsapp:+1234567890&To=whatsapp:+0987654321")

if [[ "$resource_response" == *"Study Notes"* ]]; then
    echo "✅ Resources Test: Working"
else
    echo "❌ Resources Test: Failed"
fi
echo ""

# Summary
echo "📊 Test Summary"
echo "==============="
echo "🎯 Next Steps:"
echo "  1. Activate n8n workflow in interface (http://localhost:5678)"
echo "  2. Update Twilio webhook to: $N8N_URL"
echo "  3. Test with real WhatsApp messages"
echo "  4. Monitor n8n executions for analytics"
echo ""
echo "🔧 Configuration Files Created:"
echo "  - TWILIO_WEBHOOK_CONFIG.md (Twilio setup guide)"
echo "  - integration_test.sh (This test script)"
echo ""