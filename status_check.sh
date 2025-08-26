#!/bin/bash

echo "🔍 WHATSAPP BOT STATUS CHECK"
echo "============================"
echo "Time: $(date)"
echo ""

# Check services
echo "📋 SERVICE STATUS:"
echo "=================="

# Check n8n
if curl -s http://localhost:5678/ > /dev/null 2>&1; then
    echo "✅ n8n: Running on localhost:5678"
else
    echo "❌ n8n: Not accessible"
fi

# Check Flask
if curl -s http://localhost:5001/ > /dev/null 2>&1; then
    echo "✅ Flask: Running on localhost:5001"
else
    echo "❌ Flask: Not accessible"
fi

# Check ngrok
NGROK_URL=""
if curl -s http://localhost:4040/api/tunnels > /dev/null 2>&1; then
    NGROK_URL=$(curl -s "http://localhost:4040/api/tunnels" | grep -o '"public_url":"[^"]*https[^"]*' | cut -d'"' -f4)
    if [ -n "$NGROK_URL" ]; then
        echo "✅ ngrok: Active - $NGROK_URL"
    else
        echo "⚠️  ngrok: Running but no HTTPS tunnel found"
    fi
else
    echo "❌ ngrok: Not accessible"
fi

echo ""
echo "🧪 QUICK TESTS:"
echo "==============="

# Test 1: n8n local webhook
echo "Test 1: n8n local webhook"
RESPONSE=$(curl -s -X POST "http://localhost:5678/webhook/n8n-whatsapp-webhook" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "Body=hi&From=whatsapp:+917019345031&To=whatsapp:+14155238886" 2>/dev/null)

if [ -n "$RESPONSE" ]; then
    if [[ "$RESPONSE" == *"<?xml"* ]]; then
        echo "   ✅ Returns XML (TwiML)"
        if [[ "$RESPONSE" == *"Welcome to Student Support Bot"* ]]; then
            echo "   ✅ Correct content (not fallback)"
        else
            echo "   ⚠️  Returns fallback message"
        fi
    else
        echo "   ❌ Returns JSON instead of XML"
        echo "   Response: ${RESPONSE:0:100}..."
    fi
else
    echo "   ❌ No response"
fi

# Test 2: Flask backup
echo ""
echo "Test 2: Flask backup"
FLASK_RESPONSE=$(curl -s -X POST "http://localhost:5001/whatsapp" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "Body=hi&From=whatsapp:+917019345031&To=whatsapp:+14155238886" 2>/dev/null)

if [ -n "$FLASK_RESPONSE" ]; then
    if [[ "$FLASK_RESPONSE" == *"<?xml"* ]]; then
        echo "   ✅ Flask returns correct XML"
    else
        echo "   ❌ Flask response issue"
    fi
else
    echo "   ❌ Flask no response"
fi

# Test 3: ngrok tunnel (if available)
if [ -n "$NGROK_URL" ]; then
    echo ""
    echo "Test 3: ngrok tunnel"
    TUNNEL_RESPONSE=$(curl -s -X POST "$NGROK_URL/webhook/n8n-whatsapp-webhook" \
        -H "Content-Type: application/x-www-form-urlencoded" \
        -d "Body=hi&From=whatsapp:+917019345031&To=whatsapp:+14155238886" 2>/dev/null)
    
    if [ -n "$TUNNEL_RESPONSE" ]; then
        if [[ "$TUNNEL_RESPONSE" == *"<?xml"* ]]; then
            echo "   ✅ Tunnel returns XML"
        else
            echo "   ❌ Tunnel returns JSON: ${TUNNEL_RESPONSE:0:100}..."
        fi
    else
        echo "   ❌ Tunnel no response"
    fi
fi

echo ""
echo "🎯 SUMMARY:"
echo "==========="
if [[ "$RESPONSE" == *"<?xml"* ]] && [[ "$RESPONSE" == *"Welcome"* ]]; then
    echo "✅ n8n workflow is WORKING correctly"
    echo "✅ Ready for WhatsApp integration"
    if [ -n "$NGROK_URL" ]; then
        echo "📱 Twilio webhook URL: $NGROK_URL/webhook/n8n-whatsapp-webhook"
    fi
else
    echo "⚠️  n8n workflow needs attention"
    echo "✅ Flask backup is available as fallback"
fi