#!/bin/bash

echo "🧪 Testing n8n Webhook After Activation"
echo "======================================="

# Test greeting message
echo "Testing greeting message 'hi'..."
response=$(curl -s -X POST https://06945024e292.ngrok-free.app/webhook/n8n-whatsapp-webhook \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -H "ngrok-skip-browser-warning: true" \
  -d "Body=hi&From=whatsapp:+1234567890&To=whatsapp:+0987654321")

if [[ $response == *"<Message>"* ]]; then
    echo "✅ SUCCESS: n8n webhook is working!"
    echo "Response contains TwiML message"
    if [[ $response == *"Welcome to Student Support Bot"* ]]; then
        echo "✅ ROUTING FIXED: Greeting message working correctly!"
    else
        echo "⚠️  Response received but may still be fallback"
    fi
else
    echo "❌ FAILED: No TwiML response received"
    echo "Response: $response"
fi

echo ""
echo "Testing FAQ message 'fees'..."
faq_response=$(curl -s -X POST https://06945024e292.ngrok-free.app/webhook/n8n-whatsapp-webhook \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -H "ngrok-skip-browser-warning: true" \
  -d "Body=fees&From=whatsapp:+1234567890&To=whatsapp:+0987654321")

if [[ $faq_response == *"Fee Structure"* ]]; then
    echo "✅ SUCCESS: FAQ routing working correctly!"
else
    echo "⚠️  FAQ test: May need further routing optimization"
fi

echo ""
echo "🎯 Next step: Update Twilio webhook if tests pass!"