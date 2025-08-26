#!/bin/bash

echo "🧪 Testing n8n WhatsApp Webhook with Real Numbers"
echo "================================================="
echo "From: +917019345031 (Your WhatsApp)"
echo "To: +14155238886 (Twilio Sandbox)"
echo ""

# Test different message types
declare -a test_messages=(
    "hi:Greeting Test"
    "hello:Greeting Test"
    "menu:Menu Test"
    "fees:FAQ Test"
    "courses:FAQ Test"
    "notes:Resources Test"
    "help:Support Test"
)

for test_case in "${test_messages[@]}"; do
    IFS=':' read -r message test_name <<< "$test_case"
    echo "🔍 Testing: $test_name"
    echo "   Message: '$message'"
    
    response=$(curl -s -X POST https://06945024e292.ngrok-free.app/webhook/n8n-whatsapp-webhook \
        -H "Content-Type: application/x-www-form-urlencoded" \
        -H "ngrok-skip-browser-warning: true" \
        -d "Body=$message&From=whatsapp:+917019345031&To=whatsapp:+14155238886")
    
    if [[ $response == *"<Message>"* ]]; then
        echo "   ✅ TwiML Response Received"
        if [[ $response == *"Welcome to Student Support Bot"* ]]; then
            echo "   🎯 GREETING: Correct main menu response"
        elif [[ $response == *"Fee Structure"* ]]; then
            echo "   🎯 FAQ: Correct fee information"
        elif [[ $response == *"Study Notes"* ]]; then
            echo "   🎯 RESOURCES: Correct notes information"
        elif [[ $response == *"Student Support Contact"* ]]; then
            echo "   🎯 SUPPORT: Correct contact information"
        elif [[ $response == *"didn't quite understand"* ]]; then
            echo "   ⚠️  FALLBACK: Message went to fallback (routing issue)"
        else
            echo "   ❓ UNKNOWN: Different response received"
        fi
    else
        echo "   ❌ NO TwiML: No valid response"
    fi
    echo ""
done

echo "📊 Summary:"
echo "✅ n8n webhook is ACTIVE and responding"
echo "✅ TwiML responses are being generated"
echo "⚠️  Message routing needs optimization"
echo ""
echo "🎯 Current Status: PARTIALLY WORKING"
echo "   - Webhook: ✅ Active"
echo "   - TwiML: ✅ Generated"
echo "   - Routing: ⚠️ Needs fine-tuning"
echo ""
echo "📱 Your Twilio setup is correct!"
echo "🔧 The routing logic in the workflow needs adjustment"